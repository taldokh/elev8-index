import os
import pandas as pd

# Configurable parameters
TOP_Y_FIRMS = 8  # Number of top firms to select
TOP_X_STOCKS = 5  # Number of top stocks per firm

# Function to load coverpage.tsv and create a mapping of ACCESSION_NUMBER → Firm Name
def load_firm_mapping(quarter_directory):
    coverpage_path = os.path.join(quarter_directory, "coverpage.tsv")

    if os.path.exists(coverpage_path):
        coverpage_df = pd.read_csv(coverpage_path, sep='\t', dtype=str)
        firm_mapping = coverpage_df.set_index("ACCESSION_NUMBER")["FILINGMANAGER_NAME"].to_dict()
        return firm_mapping
    else:
        print(f"Missing coverpage in {quarter_directory}")
        return {}

# Function to extract stock data and attach firm name
def extract_stock_data(quarter_directory, firm_mapping):
    infotable_path = os.path.join(quarter_directory, "infotable.tsv")

    if os.path.exists(infotable_path):
        infotable_df = pd.read_csv(infotable_path, sep='\t')

        # Extract necessary columns
        stocks = infotable_df[['ACCESSION_NUMBER', 'NAMEOFISSUER', 'CUSIP', 'VALUE']]

        # Convert VALUE to numeric safely
        stocks.loc[:, 'VALUE'] = pd.to_numeric(stocks['VALUE'], errors='coerce')

        stocks = stocks.copy()  # Ensure it's a new DataFrame before modification
        stocks['FIRM_NAME'] = stocks['ACCESSION_NUMBER'].map(firm_mapping)

        # Drop rows where firm name couldn't be found
        stocks = stocks.dropna(subset=['FIRM_NAME']).copy()  # <- Copy ensures it's a new DataFrame

        return stocks
    else:
        print(f"Missing infotable in {quarter_directory}")
        return pd.DataFrame()

# Function to iterate through each quarter directory and process the stock data
def extract_stocks_from_quarter(quarter_directory):
    firm_mapping = load_firm_mapping(quarter_directory)
    stocks_df = extract_stock_data(quarter_directory, firm_mapping)

    # **Fix: Sum stock values per firm to avoid duplicates**
    stocks_df = stocks_df.groupby(['FIRM_NAME', 'NAMEOFISSUER', 'CUSIP'], as_index=False)['VALUE'].sum()

    return stocks_df

# Main function to process each quarter and generate index holdings
def generate_index_holdings(fillings_directory, output_file_path="Index_Holdings.xlsx"):
    all_quarters_data = []

    quarter_directories = [os.path.join(fillings_directory, d) for d in os.listdir(fillings_directory) if os.path.isdir(os.path.join(fillings_directory, d))]

    for quarter_directory in quarter_directories:
        print(f"Processing {quarter_directory}...")

        stocks_df = extract_stocks_from_quarter(quarter_directory)
        if stocks_df.empty:
            continue

        # **Step 1: Select top Y firms by total holdings**
        firm_totals = stocks_df.groupby("FIRM_NAME")["VALUE"].sum().reset_index()
        top_firms = firm_totals.nlargest(TOP_Y_FIRMS, "VALUE")["FIRM_NAME"]

        # **Step 2: Filter only the selected firms**
        stocks_df = stocks_df[stocks_df["FIRM_NAME"].isin(top_firms)]

        # **Step 3: Recalculate total firm holdings after summing stock values**
        stocks_df["TOTAL_FIRM_VALUE"] = stocks_df.groupby("FIRM_NAME")["VALUE"].transform("sum")

        # **Step 4: Calculate stock percentage within each firm**
        stocks_df["PERCENTAGE"] = (stocks_df["VALUE"] / stocks_df["TOTAL_FIRM_VALUE"]) * 100

        # **Step 5: Select the top X stocks per firm**
        stocks_df = stocks_df.sort_values(["FIRM_NAME", "PERCENTAGE"], ascending=[True, False]) \
                             .groupby("FIRM_NAME").head(TOP_X_STOCKS)

        # Store quarter information
        stocks_df["QUARTER"] = os.path.basename(quarter_directory)

        all_quarters_data.append(stocks_df)

    # **Merge all quarters into one DataFrame**
    final_df = pd.concat(all_quarters_data, ignore_index=True)

    # **Export to Excel with one sheet per quarter**
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for quarter, df in final_df.groupby("QUARTER"):
            df.to_excel(writer, sheet_name=quarter, index=False)

    print(f"Data exported to {output_file_path}")

def generate_equities_file():
    fillings_directory = "./fillings"
    generate_index_holdings(fillings_directory)
