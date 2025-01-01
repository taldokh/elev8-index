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

# Input the firm name
firm_name = "VANGUARD GROUP INC"  # Replace with the name of the desired firm

# Get the accession numbers for the selected firm in Q3 2023
firm_accession_numbers = q3_2023_filings[q3_2023_filings['FILINGMANAGER_NAME'] == firm_name]['ACCESSION_NUMBER']

# Filter INFOTABLE for these Q3 2023 filings
firm_portfolio = infotable_df[infotable_df['ACCESSION_NUMBER'].isin(firm_accession_numbers)]

# Calculate the total value of the firm's portfolio
total_portfolio_value = firm_portfolio['VALUE'].sum()

# Add a percentage column
firm_portfolio['PERCENTAGE'] = (firm_portfolio['VALUE'] / total_portfolio_value) * 100

# Sort the portfolio by percentage in descending order
firm_portfolio = firm_portfolio[['NAMEOFISSUER', 'VALUE', 'PERCENTAGE']].sort_values(by='PERCENTAGE', ascending=False)

# Display the stocks held and their percentages
print(firm_portfolio)

# Export the data to Excel
output_file = f"{firm_name}_Holdings_Q3_2023.xlsx"
firm_portfolio.to_excel(output_file, index=False)

# Display success message
print(f"Data has been exported to {output_file}.")
