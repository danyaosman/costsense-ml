from fastapi import FastAPI, HTTPException
import joblib
from pathlib import Path

app = FastAPI(title="CostSense ML Service")

# Load models at startup
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

MODELS = {
    "food": {
        "name": "Food And Beverages",
        "model": joblib.load(MODEL_DIR / "food_cpi_sarima.pkl"),
    },
    "rent": {
        "name": "Rent",
        "model": joblib.load(MODEL_DIR / "rent_cpi_sarima.pkl"),
    },
    "transport": {
        "name": "Transport",
        "model": joblib.load(MODEL_DIR / "transport_cpi_sarima.pkl"),
    },
}

# Forecast endpoint
@app.get("/forecast/{category}")
def forecast(category: str, months: int = 3):
    if category not in MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not supported"
        )

    model = MODELS[category]["model"]
    category_name = MODELS[category]["name"]

    forecast = model.get_forecast(steps=months)
    pred = forecast.predicted_mean
    ci = forecast.conf_int()

    # Last observed CPI value
    prev = float(model.data.endog[-1])

    results = []
    for date in pred.index:
        current = float(pred.loc[date])
        inflation_pct = ((current - prev) / prev) * 100

        results.append({
            "date": date.strftime("%Y-%m"),
            "cpi": round(current, 2),
            "inflation_pct": round(inflation_pct, 2),
            "lower": round(float(ci.loc[date].iloc[0]), 2),
            "upper": round(float(ci.loc[date].iloc[1]), 2),
        })

        prev = current

    return {
        "category": category_name,
        "months": months,
        "forecast": results
    }
