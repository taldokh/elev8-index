import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
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
    quarter = quarter_str[-2:]
    quarter_date = quarter_to_date.get(quarter)

    if quarter_date:
        return f"{year}{quarter_date}"
    else:
        raise ValueError(f"Invalid quarter string: {quarter_str}")


def calculate_weights_for_quarter(df):
    """Calculate the weight for each ticker in a quarter."""
    # Count unique equities in the quarter
    unique_equities = df["TICKER"].nunique()

    # Calculate equal weight per equity
    equal_weight = 100 / len(df["TICKER"])

    # Aggregate weights for duplicate tickers
    #df = df.groupby("TICKER", as_index=False).agg({"CUSIP": "first"})
    df["WEIGHT"] = df["TICKER"].map(df["TICKER"].value_counts() * equal_weight)

    # Round to 4 decimal places
    df["WEIGHT"] = df["WEIGHT"].round(4)

    df.drop_duplicates(subset=['CUSIP'], inplace=True)
    return df


def process_excel_and_insert(config_id: int):
    """Read the Excel file, map CUSIP to Ticker, calculate weight, and insert into PostgreSQL."""
    if not os.path.exists(cg.RESULT_EQUITIES_FILE_PATH):
        raise FileNotFoundError(f"Missing {cg.RESULT_EQUITIES_FILE_PATH}")

    cusip_ticker_map = load_cusip_ticker_mapping()
    all_equities = []

    # Read all sheets (quarters)
    with pd.ExcelFile(cg.RESULT_EQUITIES_FILE_PATH) as xls:
        for quarter in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=quarter)

            # Map CUSIP to Ticker
            df["TICKER"] = df["CUSIP"].map(cusip_ticker_map)

            # Drop rows where ticker is missing
            df.dropna(subset=["TICKER"], inplace=True)

            # Get the first date of the quarter
            formatted_quarter_date = get_quarter_start_date(quarter)

            # Calculate weight for each ticker
            df = calculate_weights_for_quarter(df)

            # Append to all_data list
            for _, row in df.iterrows():
                equity = Equity(
                    ticker=row["TICKER"],
                    quarter=formatted_quarter_date,
                    weight=row["WEIGHT"],
                    configuration_id=config_id
                )
                all_equities.append(equity)

    # Insert into PostgreSQL
    insert_into_db(all_equities)


def insert_into_db(all_equities):
    try:
        session.add_all(all_equities)
        session.commit()
        print(f"Inserted {len(all_equities)} records successfully.")
    except Exception as e:
        session.close()
        print(f"Database error: {e}")


def delete_all_equities():
    try:
        session.query(Equity).delete()
        session.commit()
        print("Deleted all rows in equities table.")
        print("All rows in the equities table have been deleted.")
    except Exception as e:
        session.close()
        print(f"Error deleting rows: {e}")


def insert_equities_to_db_equal_weight(config_id: int):
    print(f'processing {cg.RESULT_EQUITIES_FILE_PATH} and inserting to DB with equal weight')
    process_excel_and_insert(config_id)

