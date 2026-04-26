import pandas as pd 
import numpy
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


#print(payload.keys())
#print(type(payload['data']))
#print(payload['data'][1].keys())

def extract_freds(series_id: str, api_key :str, observation_start: str):
    params ={
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": observation_start
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()          

    payload = response.json()            
    observations = payload.get("observations", [])

    rows = []
    for obs in observations:
        rows.append({
            "series_id": series_id,
            "date": obs.get("date"),
            "value": obs.get("value")
        })

    return rows, payload


def save_raw_data(payload, out_dir="data/raw"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    fp = Path(out_dir) / f"fred_raw_{ts}.json"
    with open(fp, "w") as f:
        json.dump(payload, f)
    return fp

def save_extracted_data(rows, out_dir="data/extracted"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    fp = Path(out_dir) / f"fred_extracted_{ts}.csv"
    pd.DataFrame(rows).to_csv(fp, index=False)
    return fp