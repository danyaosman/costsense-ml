import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
from pathlib import Path

print("train_model.py started")

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# Datasets to train
DATASETS = {
    "food": "food_cpi_ts.csv",
    "rent": "rent_cpi_ts.csv",
    "transport": "transport_cpi_ts.csv",
}

def train_sarima(ts):
    model = SARIMAX(
        ts,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    return model.fit(disp=False)

for name, filename in DATASETS.items():
    print(f"\nTraining {name} model...")

    data_path = DATA_DIR / filename

    ts_df = pd.read_csv(data_path, parse_dates=["date"])
    ts = ts_df.set_index("date")["cpi"].astype(float)
    ts = ts.asfreq("MS")
    ts = ts.loc["2007-01-01":]

    results = train_sarima(ts)

    model_path = MODEL_DIR / f"{name}_cpi_sarima.pkl"
    joblib.dump(results, model_path)

    print(f"✔ Saved model to {model_path}")
    print(results.summary())

print("\nAll models trained successfully.")
