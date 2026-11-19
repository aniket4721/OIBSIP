# OIBSIP Level 2 – Task 1: House Price Prediction

## Project overview
This beginner-friendly project predicts a house's estimated price using a **Linear Regression** machine-learning model.

> **Dataset note:** `data/house_prices.csv` is a synthetic practice dataset created for this project. It is not real market or property-listing data. The model's results are for learning and demonstration only, not for financial or purchase decisions.

## Tools
- Python
- Pandas and NumPy
- Matplotlib and Seaborn (for optional visual exploration)
- Scikit-learn
- Joblib
- VS Code / Jupyter Notebook

## Dataset columns
| Column | Meaning |
|---|---|
| `Area_sqft` | House area in square feet |
| `Bedrooms` | Number of bedrooms |
| `Bathrooms` | Number of bathrooms |
| `House_Age_years` | Age of the house in years |
| `Parking_Spaces` | Number of parking spaces |
| `Price_INR` | Target house price in Indian rupees |

## Project workflow
1. Load and inspect the dataset.
2. Select house characteristics as features (`X`) and price as the target (`y`).
3. Split data into 80% training and 20% testing sets.
4. Train a Linear Regression model.
5. Predict prices for the test data.
6. Evaluate with MAE, MSE, RMSE, and R².
7. Save predictions, metrics, and the trained model.

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/house_price_prediction.py
```

## Example prediction
The script also estimates the price of an example 1,500 sq. ft. house with 3 bedrooms, 2 bathrooms, 5 years of age, and 1 parking space.

## Project structure
```text
OIBSIP-L2-Task1-HousePricePrediction/
├── data/
│   └── house_prices.csv
├── model/
│   └── linear_regression_model.joblib
├── outputs/
│   ├── sample_predictions.csv
│   └── sample_model_metrics.json
├── screenshots/
├── src/
│   └── house_price_prediction.py
├── House_Price_Prediction.ipynb
├── README.md
└── requirements.txt
```

## Important
The model is trained on a small synthetic dataset with simplified relationships. Real house prices depend on many additional factors, including location, property condition, market conditions, and local regulations.
