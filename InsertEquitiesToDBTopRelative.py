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
RESULT_EXCEL_FILE = "Index_Holdings_Tercile.xlsx"
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

            if "PERCENTAGE" not in df.columns:
                raise KeyError(f"Missing 'PERCENTAGE' column in {quarter}")

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

            # Store results
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

insert_equities_to_db()