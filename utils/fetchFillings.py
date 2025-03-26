import os
import requests
import zipfile
import shutil
import xml.etree.ElementTree as ET

# Base URL for downloading 13F data sets (correct format)
BASE_URL = "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/"

# Function to download a ZIP file
def download_zip(url, dest_folder):
    session = requests.Session()

    # Setting headers including User-Agent, Referer, and Accept
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'application/zip, application/octet-stream',
        'Referer': 'https://www.sec.gov/files/structureddata/data/form-13f-data-sets/',
    }
    session.headers.update(headers)
    response = session.get(url)
    if response.status_code == 200:
        zip_path = os.path.join(dest_folder, os.path.basename(url))
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        return zip_path
    else:
        print(f"Failed to download {url}")
        return None

# Function to extract XML files from a ZIP archive
def extract_xml(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Function to parse XML and extract COVERPAGE and INFOTABLE
def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract COVERPAGE data (example: filing date)
    coverpage = root.find('.//{http://www.sec.gov/edgar/document/thirteenf}coverPage')
    filing_date = coverpage.find('.//{http://www.sec.gov/edgar/document/thirteenf}dateFiled').text if coverpage is not None else 'UnknownDate'

    # Extract INFOTABLE data (example: holdings)
    infotable = root.findall('.//{http://www.sec.gov/edgar/document/thirteenf}infoTable')
    holdings = []
    for item in infotable:
        name = item.find('.//{http://www.sec.gov/edgar/document/thirteenf}nameOfIssuer').text
        value = item.find('.//{http://www.sec.gov/edgar/document/thirteenf}value').text
        holdings.append((name, value))

    return filing_date, holdings

# Function to process each year's quarters
def process_year(year):
    for quarter in range(1, 5):
        quarter_str = f"q{quarter}"
        dir_name = f"{year}{quarter_str}"
        dir_path = os.path.join(os.getcwd(), dir_name)
        os.makedirs(dir_path, exist_ok=True)

        # Construct the URL for the ZIP file using the new URL format
        zip_url = f"{BASE_URL}{year}{quarter_str}_form13f.zip"
        zip_path = download_zip(zip_url, dir_path)

        if zip_path:
            extract_xml(zip_path, dir_path)
            os.remove(zip_path)  # Clean up ZIP file

            # Process XML files
            for xml_file in os.listdir(dir_path):
                if xml_file.endswith('.xml'):
                    xml_path = os.path.join(dir_path, xml_file)
                    filing_date, holdings = parse_xml(xml_path)

                    # Save COVERPAGE and INFOTABLE to separate files
                    with open(os.path.join(dir_path, f"{filing_date}_coverpage.txt"), 'w') as f:
                        f.write(filing_date)

                    with open(os.path.join(dir_path, f"{filing_date}_infotable.txt"), 'w') as f:
                        for name, value in holdings:
                            f.write(f"{name}: {value}\n")

                    os.remove(xml_path)  # Clean up XML file
        else:
            print(f"Skipping quarter {quarter} of {year} due to download failure.")

# Main function to process all years from 2013 to 2023
def main():
    for year in range(2013, 2024):
        process_year(year)

if __name__ == "__main__":
    main()
