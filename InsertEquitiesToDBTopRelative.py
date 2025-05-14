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
    quarter = quarter_str[-2:]
    quarter_date = quarter_to_date.get(quarter)

    if quarter_date:
        return f"{year}{quarter_date}"
    else:
        raise ValueError(f"Invalid quarter string: {quarter_str}")


def process_excel_and_insert(config_id: int):
    """Read the Excel file, map CUSIP to Ticker, calculate weight, and insert into PostgreSQL."""
    if not os.path.exists(cg.RESULT_EQUITIES_FILE_PATH):
        raise FileNotFoundError(f"Missing {cg.RESULT_EQUITIES_FILE_PATH}")

    cusip_ticker_map = load_cusip_ticker_mapping()
    all_equities = []

    # Read all sheets (quarters)
    with pd.ExcelFile(cg.RESULT_EQUITIES_FILE_PATH) as xls:
        for quarter in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=quarter, dtype={"CUSIP": str})

            if "PERCENTAGE" not in df.columns:
                raise KeyError(f"Missing 'PERCENTAGE' column in {quarter}")

            df["CUSIP"] = df["CUSIP"].astype(str).str.strip()

            rows_to_drop = df[df["CUSIP"].map(cusip_ticker_map).isna()]
            print(f'{quarter}: null tickers: {rows_to_drop["CUSIP"]}')

            # Map CUSIP to Ticker
            df["TICKER"] = df["CUSIP"].map(cusip_ticker_map)
            df.dropna(subset=["TICKER"], inplace=True)

            # Convert percentage to decimal weight
            df["WEIGHT"] = df["PERCENTAGE"] / 100

            # Aggregate duplicate tickers
            df = df.groupby("TICKER", as_index=False)["WEIGHT"].sum()

            # Normalize weights so that the total per quarter is exactly 100
            df["WEIGHT"] = ((df["WEIGHT"] / df["WEIGHT"].sum()) * 100).round(4)

            formatted_quarter_date = get_quarter_start_date(quarter)

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


def insert_equities_to_db_relative_weight(config_id: int):
    print(f'processing {cg.RESULT_EQUITIES_FILE_PATH} and inserting to DB with relative weight')
    process_excel_and_insert(config_id)

