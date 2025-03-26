import requests
import pandas as pd
import time

def fetch_13f_filings_for_quarter(year, quarter):
    start_end_dates = {
        1: (f"{year}-01-01", f"{year}-03-31"),
        2: (f"{year}-04-01", f"{year}-06-30"),
        3: (f"{year}-07-01", f"{year}-09-30"),
        4: (f"{year}-10-01", f"{year}-12-31"),
    }
    start_date, end_date = start_end_dates.get(quarter, (None, None))

    if not start_date:
        raise ValueError("Quarter must be between 1 and 4.")

    # Updated endpoint and headers as per the latest SEC EDGAR API recommendations
    search_api_url = "https://efts.sec.gov/LATEST/search-index"
    headers = {
        "User-Agent": "MyApp/1.0 (realname@example.com)",  # Real contact info required per SEC guidelines
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json",
        "Referer": "https://www.sec.gov/"
    }

    payload = {
        "keys": ["formType"],
        "q": "formType:13F-HR",
        "startdt": start_date,
        "enddt": end_date,
        "from": 0,
        "size": 1000
    }

    response = requests.post(search_api_url, json=payload, headers=headers)
    if response.status_code == 403:
        raise ConnectionError("Access denied. Ensure User-Agent includes real contact info and check headers.")
    response.raise_for_status()

    results = response.json().get("hits", {}).get("hits", [])
    firms_data = []
    for hit in results:
        source = hit.get("_source", {})
        firms_data.append({
            "FILINGMANAGER_NAME": source.get("display_names", ["Unknown"])[0],
            "ACCESSION_NUMBER": source.get("adsh", "").replace("-", "")
        })

    return pd.DataFrame(firms_data)

def fetch_infotable(accession_number):
    url = f"https://www.sec.gov/Archives/edgar/data/{accession_number[:10]}/{accession_number}/infotable.xml"
    headers = {
        "User-Agent": "MyApp/1.0 (taldokh@gmail.com)",  # Real contact info required per SEC guidelines
        "Host": "www.sec.gov",
        "Referer": "https://www.sec.gov/"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            infotable = pd.read_xml(response.content)
            infotable["ACCESSION_NUMBER"] = accession_number
            return infotable
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

def main(year, quarter):
    output_file = f"Firms_Total_Assets_Q{quarter}_{year}.xlsx"
    firms = fetch_13f_filings_for_quarter(year, quarter)

    all_portfolios = []
    for accession in firms["ACCESSION_NUMBER"]:
        infotable = fetch_infotable(accession)
        if not infotable.empty:
            all_portfolios.append(infotable)
        time.sleep(0.2)  # Respect SEC rate limits

    if all_portfolios:
        portfolio_df = pd.concat(all_portfolios, ignore_index=True)
        portfolio = portfolio_df.merge(firms, on="ACCESSION_NUMBER", how="inner")

        firm_assets = portfolio.groupby("FILINGMANAGER_NAME")["value"].sum().reset_index()
        firm_assets = firm_assets.sort_values(by="value", ascending=False)

        firm_assets.to_excel(output_file, index=False)
        print(f"Data has been exported to {output_file}")
    else:
        print("No portfolio data available.")

if __name__ == "__main__":
    # Example usage: Fetch 13F filings for Q3 2023
    main(year=2023, quarter=3)
