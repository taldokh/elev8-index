import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Database Configuration
DB_CONFIG = {
    "host": "10.10.248.105",
    "database": "postgres",
    "user": "postgres",
    "password": "bartar20@CS"
}

# File paths
RESULT_EXCEL_FILE = "Index_Holdings.xlsx"
CUSIP_TICKER_FILE = "./fillings/cusip_tickers.csv"


def connect_db():
    """Establish a connection to PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def load_cusip_ticker_mapping():
    """Load CUSIP to Ticker mapping from CSV."""
    if not os.path.exists(CUSIP_TICKER_FILE):
        raise FileNotFoundError(f"Missing {CUSIP_TICKER_FILE}")

    cusip_ticker_df = pd.read_csv(CUSIP_TICKER_FILE, dtype=str)
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

    df.drop_duplicates(subset=['CUSIP'], inplace=True)
    return df


def process_excel_and_insert():
    """Read the Excel file, map CUSIP to Ticker, calculate weight, and insert into PostgreSQL."""
    if not os.path.exists(RESULT_EXCEL_FILE):
        raise FileNotFoundError(f"Missing {RESULT_EXCEL_FILE}")

    cusip_ticker_map = load_cusip_ticker_mapping()
    all_data = []

    # Read all sheets (quarters)
    with pd.ExcelFile(RESULT_EXCEL_FILE) as xls:
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
                all_data.append((row["TICKER"], formatted_quarter_date, row["WEIGHT"]))

    # Insert into PostgreSQL
    insert_into_db(all_data)


def insert_into_db(data):
    """Insert the processed data into PostgreSQL."""
    query = """
    INSERT INTO equities (ticker, quarter, weight)
    VALUES %s;
    """

    try:
        conn = connect_db()
        cur = conn.cursor()

        # Insert only unique (ticker, quarter) pairs, with calculated weight
        execute_values(cur, query, data)
        conn.commit()
        print(f"Inserted {len(data)} records successfully.")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()

def delete_all_equities():
    """Delete all rows from the equities table."""
    query = "DELETE FROM equities;"

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        print("All rows in the equities table have been deleted.")
    except Exception as e:
        print(f"Error deleting rows: {e}")
    finally:
        cur.close()
        conn.close()


def insert_equities_to_db():
    delete_all_equities()
    process_excel_and_insert()
