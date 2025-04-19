from types import NoneType

import psycopg2
import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import config.config as cg
from sqlalchemy import create_engine, func
from models import IndexPoint, Equity

# Database Configuration
engine = create_engine(cg.DB_CONNECTION_URL)
Session = sessionmaker(bind=engine)
session = Session()

index_history_open = {}
index_history_close = {}
latest_price = 0
latest_Date = 0


def get_quarter_ranges(start_year, end_year):
    ranges = []
    for year in range(start_year, end_year + 1):
        for i in range(len(cg.REBALANCE_DATES)):
            start_month, start_day = cg.REBALANCE_DATES[i]
            end_month, end_day = cg.REBALANCE_DATES[(i + 1) % 4]
            start_date = datetime(year if i < 3 else year, start_month, start_day)
            end_date = datetime(year if i < 3 else year + 1, end_month, end_day)
            ranges.append((start_date, end_date))
    return ranges


# Fetch the stock prices for a ticker in the given range
def fetch_prices_eod(ticker, start_date, end_date, api_token):
    url = f"https://eodhistoricaldata.com/api/eod/{ticker}.US"
    params = {
        "api_token": api_token,
        "from": start_date.strftime('%Y-%m-%d'),
        "to": end_date.strftime('%Y-%m-%d'),
        "period": "d",
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        response = requests.get(f"https://eodhistoricaldata.com/api/eod/{ticker.replace('/', '-')}.US", params=params)
        if response.status_code != 200:
            response = requests.get(f"https://eodhistoricaldata.com/api/eod/{ticker.replace('.', '-')}.US",
                                    params=params)
            if response.status_code != 200:
                response = requests.get(f"https://eodhistoricaldata.com/api/eod/{ticker.replace('-', '/')}.US",
                                        params=params)
                if response.status_code != 200:
                    print(f"❌ {ticker}: {response.status_code} {response.text}")
                    return None
    try:
        data = response.json()
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return  df["open"], df["close"]
    except Exception as e:
        print(f"⚠ Error fetching data for {ticker}: {e}")
        return None


# Calculate the index for a specific quarter based on the previous quarter's equities
def calculate_quarterly_index(start_date, end_date, initial_index_value, config_id: int):
    def calculate_index_daily_price_change(date, index_last_price):
        factor = 0

        if not is_trading_day(date):
            raise ValueError(f'no market traffic in that date {date}')

        for ticker, weight in tickers_weights.items():
            series_open = prices_open.get(ticker)
            series_close = prices_close.get(ticker)
            if series_open is None or series_close is None: continue

            p_open = series_open.get(date)
            p_close = series_close.get(date)
            if not p_open or not p_close:
                p_open = p_close = 1
            if pd.notna(p_close) and pd.notna(p_open) and p_open != 0:
                factor += (p_close / p_open) * (float(weight) / 100)

        return index_last_price * factor

    def calculate_index_nightly_price_change(last_active_date, current_date, index_last_price):
        factor = 0

        if not is_trading_day(current_date):
            raise ValueError(f'no market traffic in that date {current_date}')

        for ticker, weight in tickers_weights.items():
            series_open = prices_open.get(ticker)
            series_close = prices_close.get(ticker)
            if series_open is None or series_close is None: continue

            p_open = series_open.get(current_date)
            p_close = series_close.get(last_active_date)
            if not p_open or not p_close:
                p_open = p_close = 1
            if pd.notna(p_close) and pd.notna(p_open) and p_close != 0:
                factor += (p_open / p_close) * float(weight / 100)

        return index_last_price * factor

    def insert_index_to_db(day_start_points, day_end_points, date, config_id):
        try:
            index_point = IndexPoint(
                day_start_points=int(round(day_start_points)),
                day_end_points=int(round(day_end_points)),
                market_date=date.date(),
                configuration_id=config_id
            )
            session.add(index_point)
            session.commit()
        except Exception as e:
            session.close()
            print(f"Database error: {e}")

    def is_trading_day(date):
        ticker = next(iter(tickers_weights.keys()))
        test = prices_open.get(ticker)
        if date in prices_open.get(ticker):
            return True
        return False

    global index_history_open
    global index_history_close
    global latest_price
    global latest_Date

    # Get the most recent quarter <= start_date
    subquery = (
        session.query(func.max(Equity.quarter))
        .filter(Equity.quarter <= start_date)
        .scalar_subquery()
    )

    # Fetch tickers and weights for that quarter
    rows = session.query(Equity.ticker, Equity.weight).filter(Equity.quarter == subquery, Equity.configuration_id == config_id).all()
    tickers_weights = {row[0]: row[1] for row in rows}
    tickers = list(tickers_weights.keys())

    prices_open = {}
    prices_close = {}
    for i, ticker in enumerate(tickers):
        print(f"🔍 Fetching data for {ticker} ({i + 1}/{len(tickers)})")
        price_series_open, price_series_close = fetch_prices_eod(ticker, start_date, end_date, cg.EOD_API_TOKEN)
        if price_series_open is not None or price_series_close is not None:
            prices_open[ticker] = price_series_open
            prices_close[ticker] = price_series_close

    if not prices_open or not prices_close:
        print("❌ No prices found for this quarter.")
        return initial_index_value

    for date in pd.date_range(start=start_date, end=end_date - timedelta(days=1), freq="B"):
        global latest_Date
        global latest_price
        if not is_trading_day(date):
            continue
        try:
            if not index_history_open.get(date):
                if date == end_date:
                    index_history_open[date] = latest_price = calculate_index_nightly_price_change(last_active_date=latest_Date ,current_date=date, index_last_price=latest_price)
                    index_history_close[date] = latest_price = calculate_index_daily_price_change(date=date, index_last_price=latest_price)
                    latest_Date = date
                else:
                    index_history_open[date] = latest_price = calculate_index_nightly_price_change(last_active_date=latest_Date, current_date=date, index_last_price=latest_price)
                    index_history_close[date] = latest_price = calculate_index_daily_price_change(date=date, index_last_price=latest_price)
                    latest_Date = date
                    index_history_open[date + pd.offsets.BDay(1)] = latest_price = calculate_index_nightly_price_change(last_active_date=latest_Date, current_date=date + pd.offsets.BDay(1), index_last_price=latest_price)
            else:
                if date == end_date:
                    index_history_close[date] = latest_price = calculate_index_daily_price_change(date=date, index_last_price=latest_price)
                    latest_Date = date
                else:
                    index_history_close[date] = latest_price = calculate_index_daily_price_change(date=date, index_last_price=latest_price)
                    latest_Date = date
                    index_history_open[date + pd.offsets.BDay(1)] = latest_price = calculate_index_nightly_price_change(last_active_date=latest_Date, current_date=date + pd.offsets.BDay(1), index_last_price=latest_price)
        except ValueError as e:
            print(f"{e}")
            continue

    for date in pd.date_range(start=start_date, end=end_date - timedelta(days=1), freq="B"):
        if date == cg.INDEX_CREATION_DATE:
            insert_index_to_db(initial_index_value, index_history_close[date], date, config_id)
        else:
            if is_trading_day(date):
                insert_index_to_db(index_history_open[date], index_history_close[date], date, config_id)


def delete_index_points():
    try:
        session.query(IndexPoint).delete()
        session.commit()
        print("All rows in the index_points table have been deleted.")
    except Exception as e:
        session.close()
        print(f"Database error: {e}")

def generate_quarter_ranges(start_date, end_date):
    quarter_ranges = []
    start_year = start_date.year
    end_year = end_date.year
    # Loop through each year from the start year to the end year
    for year in range(start_year, end_year + 1):
        for i, (month, day) in enumerate(cg.REBALANCE_DATES):
            # Check if the quarter start date is within the given range
            quarter_start_date = datetime(year, month, day)
            # If the quarter starts in November, it might belong to the next year
            if month == 11:
                quarter_start_date = datetime(year, month, day)
                quarter_end_date = datetime(year + 1, 2, 15)  # Next year's February
            else:
                quarter_end_date = datetime(year, cg.REBALANCE_DATES[(i + 1) % 4][0], cg.REBALANCE_DATES[(i + 1) % 4][1])
            # Skip quarters that are outside the start and end date range
            if quarter_start_date < start_date or quarter_start_date > end_date:
                continue  # This quarter is outside the range
            # Adjust quarter end date if it exceeds the provided end_date
            if quarter_end_date > end_date:
                quarter_end_date = end_date
            quarter_ranges.append((quarter_start_date, quarter_end_date))
    return quarter_ranges

def calculate_index_points(config_id: int):
    global index_history_open
    global index_history_close
    global latest_price
    global latest_Date

    latest_price = cg.INDEX_INITIAL_PRICE

    index_history_open = {}
    index_history_close = {}

    quarter_ranges = generate_quarter_ranges(cg.INDEX_CREATION_DATE, cg.INDEX_END_DATE)
    latest_Date = cg.INDEX_CREATION_DATE

    index_history_open[cg.INDEX_CREATION_DATE] = latest_price


    for start, end in quarter_ranges:
        if end < datetime.now():
            initial_value = calculate_quarterly_index(start_date=start, end_date=end, initial_index_value=latest_price, config_id=config_id)
        else:
            break