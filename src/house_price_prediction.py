from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "house_prices.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = PROJECT_ROOT / "model"
OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# 1. Load dataset
df = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully!")
print("\\nFirst five rows:")
print(df.head())
print("\\nDataset information:")
print(df.info())
print("\\nMissing values:")
print(df.isnull().sum())

# 2. Prepare features (X) and target (y)
features = ["Area_sqft", "Bedrooms", "Bathrooms",
            "House_Age_years", "Parking_Spaces"]
X = df[features]
y = df["Price_INR"]

# 3. Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Predict house prices
predictions = model.predict(X_test)

# 6. Evaluate model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

metrics = {
    "MAE_INR": float(mae),
    "MSE": float(mse),
    "RMSE_INR": float(rmse),
    "R2_Score": float(r2)
}

print("\\nModel Evaluation:")
for name, value in metrics.items():
    print(f"{name}: {value:,.4f}")

# 7. Save predictions, metrics, and trained model
prediction_report = X_test.copy()
prediction_report["Actual_Price_INR"] = y_test.values
prediction_report["Predicted_Price_INR"] = predictions.round(0).astype(int)
prediction_report.to_csv(OUTPUT_DIR / "predictions.csv", index=False)

with open(OUTPUT_DIR / "model_metrics.json", "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

joblib.dump(model, MODEL_DIR / "linear_regression_model.joblib")

print("\\nSaved predictions to outputs/predictions.csv")
print("Saved metrics to outputs/model_metrics.json")
print("Saved model to model/linear_regression_model.joblib")

# 8. Example prediction for a new house
new_house = pd.DataFrame([{
    "Area_sqft": 1500,
    "Bedrooms": 3,
    "Bathrooms": 2,
    "House_Age_years": 5,
    "Parking_Spaces": 1
}])
estimated_price = model.predict(new_house)[0]
print(f"\\nEstimated price for example house: ₹{estimated_price:,.0f}")
