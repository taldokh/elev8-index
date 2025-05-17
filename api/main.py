# app/main.py
import os
from datetime import date
from fastapi import FastAPI, BackgroundTasks, Depends, Query
from pydantic import BaseModel
import subprocess
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql.operators import and_

from main import backtest
from models import (Configuration, IndexPoint)
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware


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