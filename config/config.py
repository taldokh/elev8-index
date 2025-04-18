#DB
DB_HOST = '10.10.248.105'
DB_NAME = 'postgres'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'bartar20%40CS'
DB_CONNECTION_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

# File paths
RESULT_EQUITIES_FILE_PATH = "Index_Holdings.xlsx"
CUSIP_TICKER_FILE_PATH = "./fillings/cusip_tickers.csv"
FILLINGS_PATH = "./fillings"

# The rebalance dates, which happen on the 15th of the middle month of each quarter
REBALANCE_DATES = [
    (2, 15), (5, 15), (8, 15), (11, 15)
]

EOD_API_TOKEN = "67eee2ee694885.80164284"

