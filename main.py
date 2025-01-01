import pandas as pd

# Load the COVERPAGE and INFOTABLE tables
coverpage_file = "COVERPAGE.tsv"
infotable_file = "INFOTABLE.tsv"

coverpage_df = pd.read_csv(coverpage_file, sep='\t')
infotable_df = pd.read_csv(infotable_file, sep='\t')

# Convert the REPORTCALENDARORQUARTER column to datetime format (if not already)
coverpage_df['REPORTCALENDARORQUARTER'] = pd.to_datetime(coverpage_df['REPORTCALENDARORQUARTER'], errors='coerce')

# Define the start and end date for Q3 2023 (July 1, 2023 to September 30, 2023)
start_date = pd.to_datetime("2023-07-01")
end_date = pd.to_datetime("2023-09-30")

# Filter the COVERPAGE for filings within Q3 2023
q3_2023_filings = coverpage_df[(coverpage_df['REPORTCALENDARORQUARTER'] >= start_date) &
                                (coverpage_df['REPORTCALENDARORQUARTER'] <= end_date)]

# Extract firm name and accession number from COVERPAGE for Q3 2023
firms = q3_2023_filings[['FILINGMANAGER_NAME', 'ACCESSION_NUMBER']]

# Join with INFOTABLE on ACCESSION_NUMBER (only for Q3 2023 filings)
portfolio = infotable_df.merge(firms, left_on='ACCESSION_NUMBER', right_on='ACCESSION_NUMBER', how='inner')

# Calculate total assets for each firm
firm_assets = portfolio.groupby('FILINGMANAGER_NAME')['VALUE'].sum().reset_index()

# Sort by total assets in descending order
firm_assets = firm_assets.sort_values(by='VALUE', ascending=False)

# Export the data to Excel
output_file = "Firms_Total_Assets_Q3_2023.xlsx"
firm_assets.to_excel(output_file, index=False)

print(f"Data has been exported to {output_file}")


import requests
import pandas as pd

# SEC EDGAR API endpoint for filings
# edgar_api_url = "https://data.sec.gov/submissions/"
# headers = {
#     "User-Agent": "YourAppName/1.0 (YourEmail@example.com)"
# }
#
# # Fetch 13F-HR filings for Q3 2023
# q3_2023_filings = []
# for cik in range(1000000, 1001000):  # Adjust CIK range as needed
#     response = requests.get(f"{edgar_api_url}CIK{cik:010d}.json", headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         filings = data.get("filings", {}).get("recent", {})
#         for i, form in enumerate(filings.get("form", [])):
#             if form == "13F-HR":
#                 filing_date = filings["filingDate"][i]
#                 if "2023-07-01" <= filing_date <= "2023-09-30":
#                     q3_2023_filings.append({
#                         "CIK": data["cik"],
#                         "Filing Date": filing_date,
#                         "Accession Number": filings["accessionNumber"][i]
#                     })
#
# # Extract firm names and accession numbers
# firm_data = []
# for filing in q3_2023_filings:
#     cik = filing["CIK"]
#     response = requests.get(f"{edgar_api_url}{filing['Accession Number']}-index.json", headers=headers)
#     if response.status_code == 200:
#         form_data = response.json()
#         firm_name = form_data.get("name", "Unknown Firm")
#         firm_data.append({"Filing Manager": firm_name, "CIK": cik})
#
# firm_df = pd.DataFrame(firm_data)
#
# # Summarize total assets by firm
# firm_assets = firm_df.groupby("Filing Manager")["Assets"].sum().reset_index()
# firm_assets = firm_assets.sort_values(by="Assets", ascending=False)
#
# # Export the data to Excel
# output_file = "Firms_Total_Assets_Q3_2023.xlsx"
# firm_assets.to_excel(output_file, index=False)
#
# print(f"Data has been exported to {output_file}.")

