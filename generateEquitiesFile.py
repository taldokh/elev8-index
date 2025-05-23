import os
import pandas as pd
import config.config as cg



# Load CUSIP mapping file
def load_cusip_mapping():
    cusip_mapping_df = pd.read_csv(cg.CUSIP_TICKER_FILE_PATH, dtype=str)
    return cusip_mapping_df.set_index('CUSIP')['Ticker'].to_dict()


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
def extract_stock_data(quarter_directory, firm_mapping, cusip_mapping):
    infotable_path = os.path.join(quarter_directory, "infotable.tsv")
    if os.path.exists(infotable_path):
        infotable_df = pd.read_csv(infotable_path, sep='\t',  dtype={
        'PUTCALL': str,
        'OTHERMANAGER': str,
    })
        stocks = infotable_df[['ACCESSION_NUMBER', 'NAMEOFISSUER', 'CUSIP', 'VALUE']].copy()
        stocks.loc[:, 'VALUE'] = pd.to_numeric(stocks['VALUE'], errors='coerce')
        stocks['FIRM_NAME'] = stocks['ACCESSION_NUMBER'].map(firm_mapping)
        stocks = stocks.dropna(subset=['FIRM_NAME'])

        # Use .loc to modify CUSIP_VALID
        stocks.loc[:, 'CUSIP_VALID'] = stocks['CUSIP'].map(lambda x: x in cusip_mapping)

        # Filter stocks that are in the CUSIP mapping
        stocks = stocks[stocks['CUSIP_VALID']].copy()

        # Add the ticker from the CUSIP mapping
        stocks['TICKER'] = stocks['CUSIP'].map(cusip_mapping)
        return stocks
    else:
        print(f"Missing infotable in {quarter_directory}")
        return pd.DataFrame()


# Function to iterate through each quarter directory and process the stock data
def extract_stocks_from_quarter(quarter_directory, cusip_mapping):
    firm_mapping = load_firm_mapping(quarter_directory)
    stocks_df = extract_stock_data(quarter_directory, firm_mapping, cusip_mapping)
    stocks_df = stocks_df.groupby(['FIRM_NAME', 'NAMEOFISSUER', 'CUSIP'], as_index=False)['VALUE'].sum()
    return stocks_df


# Function to select top N stocks per firm
def select_top_stocks(stocks_df, equities_per_firm):
    selected_stocks = []
    for firm, group in stocks_df.groupby("FIRM_NAME"):
        group = group.sort_values("VALUE", ascending=False).reset_index(drop=True)
        selected_stocks.append(group.head(equities_per_firm))
    return pd.concat(selected_stocks)


# Main function to process each quarter and generate index holdings
def generate_index_holdings(output_file_path=cg.RESULT_EQUITIES_FILE_PATH):
    all_quarters_data = []
    quarter_directories = [os.path.join(cg.FILLINGS_PATH, d) for d in os.listdir(cg.FILLINGS_PATH) if
                           os.path.isdir(os.path.join(cg.FILLINGS_PATH, d))]
    cusip_mapping = load_cusip_mapping()

    for quarter_directory in quarter_directories:
        print(f"Processing {quarter_directory}...")
        stocks_df = extract_stocks_from_quarter(quarter_directory, cusip_mapping)
        if stocks_df.empty:
            continue

        # Filter top firms
        firm_totals = stocks_df.groupby("FIRM_NAME")["VALUE"].sum().reset_index()
        top_firms = firm_totals.nlargest(NUMBER_OF_FIRMS, "VALUE")["FIRM_NAME"]
        stocks_df = stocks_df[stocks_df["FIRM_NAME"].isin(top_firms)]
        stocks_df["TOTAL_FIRM_VALUE"] = stocks_df.groupby("FIRM_NAME")["VALUE"].transform("sum")

        # Select stocks
        selected_stocks = select_top_stocks(stocks_df, EQUITIES_PER_FIRM)
        selected_stocks["PERCENTAGE"] = (selected_stocks["VALUE"] / selected_stocks["TOTAL_FIRM_VALUE"]) * 100
        selected_stocks["QUARTER"] = os.path.basename(quarter_directory)
        all_quarters_data.append(selected_stocks)

    final_df = pd.concat(all_quarters_data, ignore_index=True)

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for quarter, df in final_df.groupby("QUARTER"):
            df.to_excel(writer, sheet_name=quarter, index=False)

    print(f"Data exported to {output_file_path}")


def generate_equities_file_top(equities_per_firm, number_of_firms):
    global EQUITIES_PER_FIRM, NUMBER_OF_FIRMS

    EQUITIES_PER_FIRM = equities_per_firm
    NUMBER_OF_FIRMS = number_of_firms

    print(f'Selecting {equities_per_firm} stocks per {number_of_firms} with the TOP selection method')
    generate_index_holdings()
