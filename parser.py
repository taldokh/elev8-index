
from models.firm_model import Firm
from models.thirteen_f_holding_model import ThirteenFHolding
import config.config as cg
import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



# --- SETUP DB ---
engine = create_engine(cg.DB_CONNECTION_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Load CUSIP to ticker mapping
cusip_map = pd.read_csv(cg.CUSIP_TICKER_FILE_PATH)
cusip_to_ticker = dict(zip(cusip_map['CUSIP'], cusip_map['Ticker']))

def parse_quarter_dir(quarter_dir):
    quarter_str = os.path.basename(quarter_dir)
    quarter_end_date = get_quarter_end_date(quarter_str)

    coverpage_path = os.path.join(quarter_dir, "COVERPAGE.tsv")
    infotable_path = os.path.join(quarter_dir, "INFOTABLE.tsv")

    if not os.path.exists(coverpage_path) or not os.path.exists(infotable_path):
        print(f"Missing files in {quarter_dir}")
        return

    df_cover = pd.read_csv(coverpage_path, sep="\t", dtype=str)
    df_info = pd.read_csv(infotable_path, sep="\t", dtype=str)

    for _, firm_row in df_cover.iterrows():
        cik = firm_row["SECFILENUMBER"]
        name = firm_row["FILINGMANAGER_NAME"]

        # Get or create firm
        firm = session.query(Firm).filter_by(cik=cik).first()
        if not firm:
            firm = Firm(cik=cik, name=name)
            session.add(firm)
            session.flush()  # so we get firm.id

        # Filter firm holdings from infotable
        firm_holdings = df_info[df_info["FORM13FFILENUMBER"] == cik]

        for _, holding_row in firm_holdings.iterrows():
            cusip = holding_row["CUSIP"].strip()
            ticker = cusip_to_ticker.get(cusip)
            if not ticker:
                continue  # skip if no mapping

            holding = ThirteenFHolding(
                firm_id=firm.id,
                ticker=ticker,
                cusip=cusip,
                name_of_issuer=holding_row.get("NAME OF ISSUER"),
                value=parse_int(holding_row.get("VALUE (x$1000)", "0")),
                shares=parse_int(holding_row.get("SHRS OR PRN AMT", "0")),
                put_call=holding_row.get("PUT/CALL"),
                discretion=holding_row.get("DISCRETION"),
                quarter=quarter_end_date
            )
            session.add(holding)

    session.commit()

def parse_int(value):
    try:
        return int(str(value).replace(",", ""))
    except:
        return 0

def get_quarter_end_date(quarter_str):
    year = int(quarter_str[:4])
    quarter = int(quarter_str[-1])
    month = quarter * 3
    day = 30 if month != 12 else 31
    return datetime(year, month, day).date()

def main():
    for quarter_folder in sorted(os.listdir(cg.FILLINGS_PATH)):
        folder_path = os.path.join(cg.FILLINGS_PATH, quarter_folder)
        if os.path.isdir(folder_path):
            print(f"Parsing {folder_path}")
            parse_quarter_dir(folder_path)

if __name__ == "__main__":
    main()
