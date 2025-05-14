import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config.config as cg
from models.equity_model import Equity

# Database Configuration
engine = create_engine(cg.DB_CONNECTION_URL)
Session = sessionmaker(bind=engine)
session = Session()


def load_cusip_ticker_mapping():
    """Load CUSIP to Ticker mapping from CSV."""
    if not os.path.exists(cg.CUSIP_TICKER_FILE_PATH):
        raise FileNotFoundError(f"Missing {cg.CUSIP_TICKER_FILE_PATH}")

    cusip_ticker_df = pd.read_csv(cg.CUSIP_TICKER_FILE_PATH, dtype=str)
    cusip_ticker_df["CUSIP"] = cusip_ticker_df["CUSIP"].str.strip()
    cusip_ticker_df["Ticker"] = cusip_ticker_df["Ticker"].str.strip().str.upper()
    return cusip_ticker_df.set_index("CUSIP")["Ticker"].to_dict()


def get_quarter_start_date(quarter_str):
    """Convert quarter string (e.g., '2023q1') to the first date of the quarter."""
    quarter_to_date = {
        "q1": "-01-01",
        "q2": "-04-01",
        "q3": "-07-01",
        "q4": "-10-01"
    }

    year = quarter_str[:4]
    quarter = quarter_str[-2:].lower()
    quarter_date = quarter_to_date.get(quarter)

    if quarter_date:
        return f"{year}{quarter_date}"
    else:
        raise ValueError(f"Invalid quarter string: {quarter_str}")


def calculate_weights_for_quarter(df):
    """Calculate the weight for each ticker based on frequency across firms."""
    # Frequency of each ticker
    ticker_counts = df["TICKER"].value_counts()

    # Total number of holdings (not unique)
    total_tickers = ticker_counts.sum()

    # Calculate proportional weight
    df["WEIGHT"] = df["TICKER"].map(lambda ticker: (ticker_counts[ticker] / total_tickers) * 100)

    # Round weights
    df["WEIGHT"] = df["WEIGHT"].round(4)

    # Drop duplicate equities (per firm per quarter)
    df.drop_duplicates(subset=['CUSIP'], inplace=True)

    return df


def process_excel_and_insert(config_id: int):
    """Read the Excel file, map CUSIP to Ticker, calculate weights, and insert into DB."""
    if not os.path.exists(cg.RESULT_EQUITIES_FILE_PATH):
        raise FileNotFoundError(f"Missing {cg.RESULT_EQUITIES_FILE_PATH}")

    cusip_ticker_map = load_cusip_ticker_mapping()
    all_equities = []

    with pd.ExcelFile(cg.RESULT_EQUITIES_FILE_PATH) as xls:
        for quarter in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=quarter, dtype={"CUSIP": str})

            df["CUSIP"] = df["CUSIP"].astype(str).str.strip()

            rows_to_drop = df[df["CUSIP"].map(cusip_ticker_map).isna()]
            print(f'{quarter}: null tickers: {rows_to_drop["CUSIP"]}')

            # Map CUSIP to Ticker
            df["TICKER"] = df["CUSIP"].map(cusip_ticker_map)

            # Drop rows with missing ticker
            df.dropna(subset=["TICKER"], inplace=True)

            # Format quarter start date
            formatted_quarter_date = get_quarter_start_date(quarter)

            # Calculate weighted holdings
            df = calculate_weights_for_quarter(df)

            for _, row in df.iterrows():
                equity = Equity(
                    ticker=row["TICKER"],
                    quarter=formatted_quarter_date,
                    weight=row["WEIGHT"],
                    configuration_id=config_id
                )
                all_equities.append(equity)

    insert_into_db(all_equities)


def insert_into_db(all_equities):
    """Insert processed equity data into the database."""
    try:
        session.add_all(all_equities)
        session.commit()
        print(f"Inserted {len(all_equities)} equity records successfully.")
    except Exception as e:
        session.rollback()
        print(f"Database error during insert: {e}")
    finally:
        session.close()


def delete_all_equities():
    """Delete all rows from the equities table."""
    try:
        session.query(Equity).delete()
        session.commit()
        print("Deleted all rows in equities table.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting equities: {e}")
    finally:
        session.close()


def insert_equities_to_db_equal_weight(config_id: int):
    """Main entry point to process and insert equities using proportional weighting."""
    print(f"Processing {cg.RESULT_EQUITIES_FILE_PATH} with proportional weights...")
    process_excel_and_insert(config_id)
