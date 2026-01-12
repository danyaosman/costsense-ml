# CostSense ML

A machine learning service for forecasting Consumer Price Index (CPI) trends using SARIMA models. This project provides time series forecasting for food, rent, and transport categories to help understand inflation and cost trends.

## Features

- **SARIMA Modeling**: Uses Seasonal AutoRegressive Integrated Moving Average (SARIMA) models for accurate CPI forecasting.
- **Multiple Categories**: Supports forecasting for food and beverages, rent, and transport CPI data.
- **FastAPI Service**: RESTful API for easy integration and real-time forecasts.
- **Confidence Intervals**: Provides prediction intervals for uncertainty quantification.
- **Inflation Calculations**: Includes percentage inflation calculations for each forecast period.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/costsense-ml.git
   cd costsense-ml
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Training the Models

Before running the service, you need to train the SARIMA models on the historical data:

```bash
python train_model.py
```

This script will:
- Load CPI time series data from the `data/` directory
- Train SARIMA models for each category (food, rent, transport)
- Save the trained models to the `models/` directory

### Running the API Service

Start the FastAPI server:

```bash
uvicorn app:app --reload --port 8001
```

The service will be available at `http://localhost:8001`.

### API Documentation

Once the server is running, visit `http://localhost:8001/docs` for interactive API documentation.

#### Forecast Endpoint

**GET** `/forecast/{category}`

Parameters:
- `category` (path): One of `food`, `rent`, or `transport`
- `months` (query, optional): Number of months to forecast (default: 3)

Example request:
```
GET http://localhost:8001/forecast/food?months=6
```

Example response:
```json
{
  "category": "Food And Beverages",
  "months": 6,
  "forecast": [
    {
      "date": "2026-02",
      "cpi": 125.45,
      "inflation_pct": 1.23,
      "lower": 123.12,
      "upper": 127.78
    },
    ...
  ]
}
```

## Data

The project uses historical CPI data stored in the `data/` directory:
- `food_cpi_ts.csv`: Food and beverages CPI time series
- `rent_cpi_ts.csv`: Rent CPI time series  
- `transport_cpi_ts.csv`: Transport CPI time series

Data format: CSV with columns `date` (YYYY-MM-DD) and `cpi` (float).

## Project Structure

```
costsense-ml/
├── app.py                 # FastAPI application
├── train_model.py         # Model training script
├── requirements.txt       # Python dependencies
├── data/                  # Historical CPI data
│   ├── food_cpi_ts.csv
│   ├── rent_cpi_ts.csv
│   └── transport_cpi_ts.csv
└── models/                # Trained model files
    ├── food_cpi_sarima.pkl
    ├── rent_cpi_sarima.pkl
    └── transport_cpi_sarima.pkl
```

## Dependencies

Key dependencies include:
- FastAPI: Web framework
- pandas: Data manipulation
- statsmodels: Statistical modeling (SARIMA)
- joblib: Model serialization
- uvicorn: ASGI server

See `requirements.txt` for the complete list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License