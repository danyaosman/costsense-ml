import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
from pathlib import Path

print("train_model.py started")
# Paths (robust)
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "food_cpi_ts.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "food_cpi_sarima.pkl"

# Load time series
ts_df = pd.read_csv(DATA_PATH, parse_dates=["date"])
ts = ts_df.set_index("date")["cpi"]
ts = ts.asfreq("MS")
ts = ts.loc["2007-01-01":]

# Train SARIMA
model = SARIMAX(
    ts,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

results = model.fit()

# Save model
joblib.dump(results, MODEL_PATH)

print(results.summary())
