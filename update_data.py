import os
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

EVDS_API_KEY = os.getenv("EVDS_API_KEY")
if not EVDS_API_KEY:
    raise RuntimeError("EVDS_API_KEY not set")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CATEGORIES = {
    "food": {
        "series": "TP.FE.OKTG01",
        "csv": "food_cpi_ts.csv",
        "value_col": "TP_FE_OKTG01",
    },
    "rent": {
        "series": "TP.FE.KIRA",
        "csv": "rent_cpi_ts.csv",
        "value_col": "TP_FE_KIRA",
    },
    "transport": {
        "series": "TP.FE.ULASTIRMA",
        "csv": "transport_cpi_ts.csv",
        "value_col": "TP_FE_ULASTIRMA",
    },
}

EVDS_URL = "https://evds2.tcmb.gov.tr/service/evds/"

# HELPERS
def fetch_evds_series(series, start_date, end_date):
    url = (
        f"{EVDS_URL}"
        f"series={series}"
        f"&startDate={start_date}"
        f"&endDate={end_date}"
        f"&type=json"
    )

    headers = {"key": EVDS_API_KEY}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    data = r.json()
    return pd.DataFrame(data.get("items", []))


def normalize_ts(df, value_col):
    """
    Convert EVDS raw dataframe into canonical:
    date (MS), cpi (float)
    """
    if df.empty:
        return df

    df = df.copy()

    # EVDS uses "Tarih"
    df["date"] = pd.to_datetime(df["Tarih"], dayfirst=True)
    df["date"] = df["date"].dt.to_period("M").dt.to_timestamp(how='start')

    df["cpi"] = pd.to_numeric(df[value_col], errors="coerce")

    df = df[["date", "cpi"]]
    df = df.dropna()
    df = df.sort_values("date")

    return df


def update_category(name, cfg):
    csv_path = DATA_DIR / cfg["csv"]

    if not csv_path.exists():
        print(f"{name}: CSV not found, skipping")
        return

    local = pd.read_csv(csv_path, parse_dates=["date"])
    last_date = local["date"].max()

    start = (last_date + timedelta(days=1)).strftime("%d-%m-%Y")
    prev_month_end = datetime.today().replace(day=1) - timedelta(days=1)
    end = prev_month_end.strftime("%d-%m-%Y")

    print(f"\nUpdating {name} from {start} to {end}")

    raw = fetch_evds_series(cfg["series"], start, end)
    new = normalize_ts(raw, cfg["value_col"])

    if new.empty:
        print(f"ℹ{name}: no new data")
        return
    """combined = pd.concat([local, new], ignore_index=True)
    combined.drop_duplicates(subset="date", inplace=True)
    combined.sort_values("date", inplace=True)

    combined.to_csv(csv_path, index=False)"""
    print(f"{name}: added {len(new)} new rows")

    

# MAIN
if __name__ == "__main__":
    for name, cfg in CATEGORIES.items():
        update_category(name, cfg)

    print("\nCPI update complete")
