
import pandas as pd
import numpy as np
import os

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Load original dataset
df = pd.read_csv("data/OIBSIP_Task3_Messy_Customer_Data.csv")

print("Original dataset loaded successfully!")

# Remove duplicate customer records
df = df.drop_duplicates(
    subset=[
        "Customer_Name", "Gender", "Age", "City",
        "Join_Date", "Annual_Income", "Spending_Score",
        "Purchase_Amount"
    ],
    keep="first"
)

# Standardise Gender
df["Gender"] = df["Gender"].str.strip().str.lower()
df["Gender"] = df["Gender"].replace({
    "m": "Male", "male": "Male",
    "f": "Female", "female": "Female"
})

# Standardise City
df["City"] = df["City"].str.strip().str.title()

# Convert dates
df["Join_Date"] = pd.to_datetime(
    df["Join_Date"],
    format="mixed",
    errors="coerce",
    dayfirst=True
)

# Convert numerical columns
numeric_columns = [
    "Age", "Annual_Income",
    "Spending_Score", "Purchase_Amount"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Correct invalid values
df.loc[~df["Age"].between(0, 100), "Age"] = np.nan
df.loc[df["Annual_Income"] <= 0, "Annual_Income"] = np.nan
df.loc[~df["Spending_Score"].between(0, 100), "Spending_Score"] = np.nan
df.loc[df["Purchase_Amount"] < 0, "Purchase_Amount"] = np.nan

# Fill missing numerical values using median
for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

# Create IQR outlier report
outlier_summary = []

for col in numeric_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    count = ((df[col] < lower) | (df[col] > upper)).sum()

    outlier_summary.append([col, lower, upper, count])

outlier_summary_df = pd.DataFrame(
    outlier_summary,
    columns=["Column", "Lower_Bound", "Upper_Bound", "Outlier_Count"]
)

# Create data quality report
quality_report = pd.DataFrame({
    "Column": df.columns,
    "Data_Type": df.dtypes.astype(str).values,
    "Missing_Values": df.isnull().sum().values
})

# Save output files
df.to_csv("outputs/cleaned_customer_data.csv", index=False)
outlier_summary_df.to_csv("outputs/outlier_summary.csv", index=False)
quality_report.to_csv("outputs/data_quality_report.csv", index=False)

print("\nData cleaning completed successfully!")
print("\nFinal missing values:")
print(df.isnull().sum())

print("\nAll output files saved in the outputs folder.")
