# from insertEquitiesToDB import insert_equities_to_db
# from generateEquitiesFile import generate_equities_file

# if __name__ == '__main__':
#     generate_equities_file()
#     insert_equities_to_db()


import requests
import pandas as pd

# --- Config ---
API_KEY = '67eee2ee694885.80164284'  # Replace with your EODHD API key
SYMBOL = 'TSLA.US'         # Format: {ticker}.{exchange}, e.g., TSLA.US or TWTR.US
FROM_DATE = '2015-11-19'
TO_DATE = '2015-11-25'

# --- API Request ---
url = f'https://eodhistoricaldata.com/api/eod/{SYMBOL}'
params = {
    'from': FROM_DATE,
    'to': TO_DATE,
    'api_token': API_KEY,
    'period': 'd',         # Daily data
    'fmt': 'json'          # You can also use 'csv'
}

response = requests.get(url, params=params)
data = response.json()

# --- Convert to DataFrame ---
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
df = df.sort_index()

# --- Show Output ---
print(df.head())  # Display first few rows
df.to_csv('historical_stock_data.csv')
print("Data saved to 'historical_stock_data.csv'")
