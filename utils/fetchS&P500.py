from datetime import datetime

import pandas as pd
import requests
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import config.config as cg
from models import IndexPoint
from models.equity_model import Equity

# --- DB SETUP ---
engine = create_engine(cg.DB_CONNECTION_URL)
Session = sessionmaker(bind=engine)
session = Session()

# --- Constants ---
def get_quarter_start_date(quarter_str):
    quarter_to_date = {
        "q1": "-01-01",
        "q2": "-04-01",
        "q3": "-07-01",
        "q4": "-10-01"
    }
    year = quarter_str[:4]
    quarter = quarter_str[-2:].lower()
    if quarter not in quarter_to_date:
        raise ValueError(f"Invalid quarter string: {quarter_str}")
    return f"{year}{quarter_to_date[quarter]}"

def get_quarterly_start_dates(start_date: datetime, end_date: datetime):
    quarters = []
    for year in range(start_date.year, end_date.year + 1):
        for q in ['q1', 'q2', 'q3', 'q4']:
            quarter_date_str = get_quarter_start_date(f"{year}{q}")
            quarter_date = datetime.strptime(quarter_date_str, '%Y-%m-%d').date()
            if start_date.date() <= quarter_date <= end_date.date():
                quarters.append(quarter_date)
    return quarters

def insert_sp500_quarterly_equities():
    start_date = cg.INDEX_CREATION_DATE
    end_date = cg.INDEX_END_DATE

    print(f"Fetching S&P500 data from {start_date.date()} to {end_date.date()}...")

    print("Determining quarterly start dates...")
    quarter_dates = get_quarterly_start_dates(start_date, end_date)

    # Fetch existing (ticker, quarter) combinations to skip duplicates
    existing_quarters = {
        row.quarter
        for row in session.query(Equity.quarter)
        .filter(and_(Equity.ticker == cg.GSPC_EOD_SYMBOL, Equity.configuration_id == cg.GSPC_CONFIG_ID))
        .all()
    }

    new_equities = []
    for quarter_date in quarter_dates:
        if quarter_date in existing_quarters:
            print(f"Skipping existing record for {quarter_date}")
            continue

        equity = Equity(
            ticker=cg.GSPC_EOD_SYMBOL,
            quarter=quarter_date,  # ← use calendar quarter date now
            weight=100.0000,
            configuration_id=cg.GSPC_CONFIG_ID
        )
        new_equities.append(equity)

    if new_equities:
        session.add_all(new_equities)
        session.commit()
        print(f"Inserted {len(new_equities)} S&P500 records.")
    else:
        print("No new records to insert.")

    session.close()

def insert_index_points_from_sp500():
    # Step 1: Fetch S&P500 EOD data
    url = f"https://eodhd.com/api/eod/{cg.GSPC_EOD_SYMBOL}?api_token={cg.EOD_API_TOKEN}&from={cg.INDEX_CREATION_DATE.strftime('%Y-%m-%d')}&to={cg.INDEX_END_DATE.strftime('%Y-%m-%d')}&period=d&fmt=json"
    response = requests.get(url)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df['date'] = pd.to_datetime(df['date']).dt.date
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    previous_points = cg.INDEX_INITIAL_PRICE
    index_rows = []

    for i, current_date in enumerate(df.index):
        if i == 0:
            # First day: base on close/open
            open_price = df.loc[current_date, 'open']
            close_price = df.loc[current_date, 'close']
            start_points = cg.INDEX_INITIAL_PRICE
            end_points = int(round(start_points * (close_price / open_price)))
        else:
            prev_close = df.loc[df.index[i - 1], 'close']
            today_close = df.loc[current_date, 'close']
            start_points = previous_points
            end_points = int(round(start_points * (today_close / prev_close)))

        index_rows.append(IndexPoint(
            day_start_points=int(round(start_points)),
            day_end_points=end_points,
            market_date=current_date,
            configuration_id=cg.GSPC_CONFIG_ID
        ))
        previous_points = end_points

    # Step 2: Insert into DB
    try:
        session.bulk_save_objects(index_rows)
        session.commit()
        print(f"✅ Inserted {len(index_rows)} index point rows.")
    except Exception as e:
        session.rollback()
        print(f"❌ DB Insert Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_sp500_quarterly_equities()
    insert_index_points_from_sp500()