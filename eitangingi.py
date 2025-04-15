import psycopg2
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

RATE_LIMIT_SLEEP = 3
BATCH_SIZE = 50


# מחזיר טווחי רבעון לפי התבנית המבוקשת
REBALANCE_DATES = [
    (2, 15), (5, 15), (8, 15), (11, 15)
]

def get_quarter_ranges(start_year, end_year):
    ranges = []
    for year in range(start_year, end_year + 1):
        for i in range(len(REBALANCE_DATES)):
            start_month, start_day = REBALANCE_DATES[i]
            end_month, end_day = REBALANCE_DATES[(i + 1) % 4]
            start_date = datetime(year if i < 3 else year, start_month, start_day)
            end_date = datetime(year if i < 3 else year + 1, end_month, end_day)
            ranges.append((start_date, end_date))
    return ranges


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
        print(f"❌ {ticker}: {response.status_code} {response.text}")
        return None
    try:
        data = response.json()
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df['adjusted_close'] if 'adjusted_close' in df.columns else df['close']
    except Exception as e:
        print(f"⚠️ שגיאה בעיבוד {ticker}: {e}")
        return None


def calculate_quarterly_index(start_date, end_date, initial_index_value, db_params, api_token):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("""
        SELECT ticker, weight
        FROM equities
        WHERE quarter = (
            SELECT MAX(quarter)
            FROM equities
            WHERE quarter <= %s
        )
    """, (end_date,))
    rows = cur.fetchall()
    tickers_weights = {row[0]: row[1] for row in rows}
    tickers = list(tickers_weights.keys())

    prices = {}
    for i, ticker in enumerate(tickers):
        print(f"🔍 מושך {ticker} ({i+1}/{len(tickers)})")
        price_series = fetch_prices_eod(ticker, start_date, end_date, api_token)
        if price_series is not None:
            prices[ticker] = price_series
        time.sleep(RATE_LIMIT_SLEEP)

    if not prices:
        print("❌ לא נמצאו מחירים לרבעון זה.")
        return initial_index_value

    valid_start = pd.Series([d for s in prices.values() for d in s.index]).value_counts().idxmax()
    print(f"📅 תאריך פתיחה בפועל: {valid_start.date()}")

    index_history = []
    for date in pd.date_range(start=start_date, end=end_date - timedelta(days=1), freq="B"):
        index_value = 0
        for ticker, weight in tickers_weights.items():
            series = prices.get(ticker)
            if series is None: continue
            p_today = series.get(date)
            p_start = series.get(valid_start)
            if pd.notna(p_today) and pd.notna(p_start) and p_start != 0:
                index_value += (p_today / p_start) * weight
        index = (index_value / sum(tickers_weights.values())) * initial_index_value
        index_history.append((index, date))

    for i, (value, date) in enumerate(index_history):
        start_point = index_history[i - 1][0] if i > 0 else initial_index_value
        cur.execute("""
            INSERT INTO index_points (day_start_points, day_end_points, market_date, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (market_date) DO UPDATE
            SET day_start_points = EXCLUDED.day_start_points,
                day_end_points = EXCLUDED.day_end_points,
                created_at = EXCLUDED.created_at
        """, (round(start_point, 2), round(value, 2), date.date(), datetime.now()))

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ עודכן רבעון: {start_date.date()} - {end_date.date()} עם סיום ב-{round(index_history[-1][0], 2)}")
    return index_history[-1][0]


# === הרצה ===
if __name__ == "__main__":
    db_params = {
        'host': '10.10.248.105',
        'dbname': 'postress',
        'user': 'postgres',
        'password': 'bartar20@CS',
        'port': 5432
    }
    api_token = "67e488357cbf89.99720911"

    initial_value = 1000
    quarter_ranges = get_quarter_ranges(datetime.now().year - 1, datetime.now().year)
    for start, end in quarter_ranges:
        if end < datetime.now():
            initial_value = calculate_quarterly_index(start, end, initial_value, db_params, api_token)
        else:
            break

         #"67e488357cbf89.99720911"