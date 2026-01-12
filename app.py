from fastapi import FastAPI
import joblib
from pathlib import Path

app = FastAPI(title="CostSense ML Service")

# Load model once at startup
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "food_cpi_sarima.pkl"

model = joblib.load(MODEL_PATH)

@app.get("/forecast/food")
def forecast_food(months: int = 3):
    forecast = model.get_forecast(steps=months)
    pred = forecast.predicted_mean
    ci = forecast.conf_int()

    last_actual = float(model.data.endog[-1])
    prev = last_actual

    results = []
    for date in pred.index:
        current = float(pred.loc[date])

        inflation_pct = ((current - prev) / prev) * 100

        results.append({
            "date": date.strftime("%Y-%m"),
            "cpi": round(current, 2),
            "inflation_pct": round(inflation_pct, 2),
            "lower": round(float(ci.loc[date][0]), 2),
            "upper": round(float(ci.loc[date][1]), 2)
        })

        prev = current

    return {
        "category": "Food And Non-Alcoholic Beverages",
        "forecast": results
    }
