# app/main.py
import os
from collections import defaultdict
from datetime import date

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, BackgroundTasks, Depends, Query, HTTPException
from pydantic import BaseModel
import subprocess
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql.operators import and_
from config import config as cg
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
from datetime import datetime

from main import backtest
from models import (Configuration, IndexPoint, Equity)
from .database import get_db


app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BacktestRequest(BaseModel):
    selection_type_top: bool
    relative_weight: bool
    equities_per_firm: int
    number_of_firms: int

def run_backtest_container(config: BacktestRequest):
    command = [
        "docker", "run", "--rm",
        "-e", f"SELECTION_TYPE_TOP={str(config.selection_type_top)}",
        "-e", f"RELATIVE_WEIGHT={str(config.relative_weight)}",
        "-e", f"EQUITIES_PER_FIRM={str(config.equities_per_firm)}",
        "-e", f"NUMBER_OF_FIRMS={str(config.number_of_firms)}",
        "--network", "host",  # or your Docker network name
        "backtest-runner"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

@app.post("/run-backtest")
def trigger_backtest(config: BacktestRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(
        backtest,
        selection_type_top=config.selection_type_top,
        relative_weight=config.relative_weight,
        equities_per_firm=config.equities_per_firm,
        number_of_firms=config.number_of_firms
    )
    return {"status": "Backtest container started"}


@app.get("/conf-exists")
def check_configuration(
    selection_type_top: bool = Query(...),
    relative_weight: bool = Query(...),
    equities_per_firm: int = Query(...),
    number_of_firms: int = Query(...),
    db: Session = Depends(get_db)
):
    config = BacktestRequest(
        selection_type_top=selection_type_top,
        relative_weight=relative_weight,
        equities_per_firm=equities_per_firm,
        number_of_firms=number_of_firms
    )
    config = db.query(Configuration).filter_by(
        selection_type_top=config.selection_type_top,
        relative_weight=config.relative_weight,
        equities_per_firm=config.equities_per_firm,
        number_of_firms=config.number_of_firms
    ).first()

    if config:
        return {"exists": True, "id": config.id}
    else:
        return {"exists": False}

@app.get("/conf-ready")
def conf_ready(conf_id: int, db: Session = Depends(get_db)):
    target_date = date(2024, 2, 13)

    exists = db.query(IndexPoint).filter_by(configuration_id=conf_id, market_date=target_date).first()

    return {"ready": bool(exists)}

@app.get("/equities-by-quarter")
def get_equities_by_quarter(config_id: int = Query(...), db: Session = Depends(get_db)):
    equities = (
        db.query(Equity)
        .filter(Equity.configuration_id == config_id)
        .order_by(Equity.quarter, Equity.weight.desc())
        .all()
    )

    result = defaultdict(list)
    for eq in equities:
        result[eq.quarter.isoformat()].append({
            "ticker": eq.ticker,
            "weight": float(eq.weight)
        })

    return result

@app.get("/index-points")
def get_index_points(config_id: int = Query(...), db: Session = Depends(get_db)):
    sp500 = aliased(IndexPoint)

    points = (
        db.query(
            IndexPoint.day_start_points,
            IndexPoint.day_end_points,
            IndexPoint.market_date,
            sp500.day_end_points.label("sp_index")
        )
        .outerjoin(
            sp500,
            and_(
                sp500.market_date == IndexPoint.market_date,
                sp500.configuration_id == 237
            )
        )
        .filter(IndexPoint.configuration_id == config_id)
        .order_by(IndexPoint.market_date)
        .all()
    )
    return [
        {
            "day_start_points": p.day_start_points,
            "day_end_points": p.day_end_points,
            "market_date": p.market_date.isoformat(),
            "sp_index": p.sp_index
        }
        for p in points
    ]

@app.get("/index-analytics")
def get_index_analytics(config_id: int = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(IndexPoint)
        .filter(IndexPoint.configuration_id == config_id)
        .order_by(IndexPoint.market_date)
        .all()
    )

    if not rows or len(rows) < 2:
        return {"error": "Not enough data to compute analytics."}

    df = pd.DataFrame([{
        "date": row.market_date,
        "value": row.day_end_points
    } for row in rows])

    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    df["daily_return"] = df["value"].pct_change()

    print(df["value"].iloc[-1])
    print(df["value"].iloc[0])
    total_return = df["value"].iloc[-1] / cg.INDEX_INITIAL_PRICE - 1
    annualized_return = (1 + total_return) ** (252 / len(df)) - 1
    annualized_volatility = df["daily_return"].std() * np.sqrt(252)
    sharpe_ratio = (
        annualized_return / annualized_volatility if annualized_volatility != 0 else 0
    )

    rolling_max = df["value"].cummax()
    drawdowns = df["value"] / rolling_max - 1
    max_drawdown = drawdowns.min()

    return {
        "total_return": round(total_return * 100, 2),  # in %
        "annualized_return": round(annualized_return * 100, 2),  # in %
        "annualized_volatility": round(annualized_volatility * 100, 2),  # in %
        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown": round(max_drawdown * 100, 2)  # in %
    }

def format_quarter(date_obj):
    year = date_obj.year
    month = date_obj.month
    quarter = (month - 1) // 3 + 1
    return f"{year}Q{quarter}"

@app.get("/export")
async def export_data(config_id: int, db: Session = Depends(get_db)):
    try:
        # Index Points
        index_points = (
            db.query(IndexPoint)
            .filter(IndexPoint.configuration_id == config_id)
            .order_by(IndexPoint.market_date)
            .all()
        )
        index_points_df = pd.DataFrame([{
            'date': point.market_date,
            'day_start_points': point.day_start_points,
            'day_end_points': point.day_end_points
        } for point in index_points])

        # Holdings
        holdings = (
            db.query(Equity)
            .filter(Equity.configuration_id == config_id)
            .order_by(Equity.quarter, Equity.weight.desc())
            .all()
        )
        holdings_df = pd.DataFrame([{
            'quarter': format_quarter(holding.quarter),
            'ticker': holding.ticker,
            'weight': holding.weight
        } for holding in holdings])

        # Analytics
        analytics = get_index_analytics(config_id, db)
        analytics_df = pd.DataFrame([analytics])

        # Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Write to sheets
            index_points_df.to_excel(writer, sheet_name='Index Points', index=False)
            holdings_df.to_excel(writer, sheet_name='Holdings', index=False)
            analytics_df.to_excel(writer, sheet_name='Analytics', index=False)

            workbook = writer.book

            # Index Points sheet formatting
            worksheet = writer.sheets['Index Points']
            for idx, col in enumerate(index_points_df.columns):
                max_len = max(
                    index_points_df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(idx, idx, max_len)

            # Holdings sheet formatting
            worksheet = writer.sheets['Holdings']
            for idx, col in enumerate(holdings_df.columns):
                max_len = max(
                    holdings_df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(idx, idx, max_len)

            # Centered format for merged quarter cells
            quarter_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            })

            # Merge quarter column rows
            merge_col_idx = 0  # 'quarter' column
            start_row = 1  # skip header row

            prev_quarter = None
            merge_start = start_row

            for i, current_quarter in enumerate(holdings_df['quarter'], start=start_row):
                if current_quarter != prev_quarter and prev_quarter is not None:
                    if i - merge_start > 1:
                        worksheet.merge_range(merge_start, merge_col_idx, i - 1, merge_col_idx, prev_quarter,
                                              quarter_format)
                    prev_quarter = current_quarter
                    merge_start = i
                elif prev_quarter is None:
                    prev_quarter = current_quarter

            # Final merge at end of data
            final_row = len(holdings_df) + start_row - 1
            if final_row - merge_start > 0:
                worksheet.merge_range(merge_start, merge_col_idx, final_row, merge_col_idx, prev_quarter)

            # Analytics sheet formatting
            worksheet = writer.sheets['Analytics']
            for idx, col in enumerate(analytics_df.columns):
                max_len = max(
                    analytics_df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(idx, idx, max_len)

        output.seek(0)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backtest_export_{config_id}_{timestamp}.xlsx"

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
