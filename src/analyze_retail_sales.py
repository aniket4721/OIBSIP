"""
OIBSIP Data Analytics - Task 1: Exploratory Data Analysis on Retail Sales
Run from this project folder:
    python src/analyze_retail_sales.py
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "dataset" / "retail_sales.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

print("\\n=== DATASET OVERVIEW ===")
print(f"Rows, columns: {df.shape}")
print("\\nColumn information:")
print(df.info())
print("\\nFirst five rows:")
print(df.head().to_string(index=False))
print("\\nMissing values by column:")
print(df.isnull().sum())
print("\\nDescriptive statistics:")
print(df.describe(include="all").to_string())

# Save monthly and quarterly trends
df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
monthly = df.groupby("Month", as_index=False)["Total Amount"].sum()
quarterly = df.groupby("Quarter", as_index=False)["Total Amount"].sum()
monthly.to_csv(OUT / "monthly_sales.csv", index=False)
quarterly.to_csv(OUT / "quarterly_sales.csv", index=False)

sns.set_theme(style="whitegrid")

# 1 monthly sales trend
plt.figure(figsize=(11,5))
plt.plot(monthly["Month"], monthly["Total Amount"], marker="o")
plt.title("Monthly Retail Sales")
plt.xlabel("Month"); plt.ylabel("Sales Amount")
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(OUT/"monthly_sales_trend.png", dpi=150); plt.close()

# 2 quarterly sales
plt.figure(figsize=(8,5))
plt.bar(quarterly["Quarter"], quarterly["Total Amount"])
plt.title("Quarterly Retail Sales")
plt.xlabel("Quarter"); plt.ylabel("Sales Amount")
plt.tight_layout(); plt.savefig(OUT/"quarterly_sales.png", dpi=150); plt.close()

# 3 category revenue
category_sales = df.groupby("Product Category", as_index=False)["Total Amount"].sum().sort_values("Total Amount", ascending=False)
category_sales.to_csv(OUT/"category_revenue.csv", index=False)
plt.figure(figsize=(9,5))
plt.bar(category_sales["Product Category"], category_sales["Total Amount"])
plt.title("Revenue by Product Category")
plt.xlabel("Product Category"); plt.ylabel("Revenue")
plt.xticks(rotation=20); plt.tight_layout()
plt.savefig(OUT/"category_revenue.png", dpi=150); plt.close()

# 4 top products by units sold
top_products = df.groupby("Product", as_index=False)["Quantity"].sum().nlargest(10,"Quantity")
top_products.to_csv(OUT/"top_10_products.csv", index=False)
plt.figure(figsize=(10,5))
plt.barh(top_products["Product"], top_products["Quantity"])
plt.title("Top 10 Products by Quantity Sold")
plt.tight_layout(); plt.savefig(OUT/"top_10_products.png", dpi=150); plt.close()

# 5 age distribution
age_df = df.dropna(subset=["Age"]).copy()
age_df["Age Group"] = pd.cut(age_df["Age"], bins=[17,25,35,45,55,100],
                             labels=["18-25","26-35","36-45","46-55","56+"])
age_counts = age_df["Age Group"].value_counts().sort_index().rename_axis("Age Group").reset_index(name="Customers")
age_counts.to_csv(OUT/"age_group_distribution.csv", index=False)
plt.figure(figsize=(8,5))
plt.bar(age_counts["Age Group"].astype(str), age_counts["Customers"])
plt.title("Transactions by Customer Age Group")
plt.tight_layout(); plt.savefig(OUT/"age_group_distribution.png", dpi=150); plt.close()

# 6 gender split
gender_counts = df["Gender"].fillna("Unknown").value_counts().rename_axis("Gender").reset_index(name="Transactions")
gender_counts.to_csv(OUT/"gender_breakdown.csv", index=False)
plt.figure(figsize=(7,5))
plt.pie(gender_counts["Transactions"], labels=gender_counts["Gender"], autopct="%1.1f%%", startangle=90)
plt.title("Transaction Split by Gender")
plt.tight_layout(); plt.savefig(OUT/"gender_breakdown.png", dpi=150); plt.close()

# 7 correlation heatmap
numeric = df[["Age","Quantity","Price per Unit","Total Amount"]].corr(numeric_only=True)
numeric.to_csv(OUT/"correlation_matrix.csv")
plt.figure(figsize=(7,5))
im = plt.imshow(numeric, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im)
plt.xticks(range(len(numeric.columns)), numeric.columns, rotation=30, ha="right")
plt.yticks(range(len(numeric.index)), numeric.index)
for i in range(len(numeric.index)):
    for j in range(len(numeric.columns)):
        plt.text(j, i, f"{numeric.iloc[i, j]:.2f}", ha="center", va="center")
plt.title("Correlation Heatmap")
plt.tight_layout(); plt.savefig(OUT/"correlation_heatmap.png", dpi=150); plt.close()

# Extra: revenue by gender
gender_revenue = df.groupby("Gender", dropna=False)["Total Amount"].sum().reset_index()
gender_revenue["Gender"] = gender_revenue["Gender"].fillna("Unknown")
plt.figure(figsize=(7,5))
plt.bar(gender_revenue["Gender"].astype(str), gender_revenue["Total Amount"])
plt.title("Revenue by Gender")
plt.tight_layout(); plt.savefig(OUT/"revenue_by_gender.png", dpi=150); plt.close()

# Basic clean copy: preserve raw data; fill missing age with median and gender with Unknown
clean = df.copy()
clean["Age"] = clean["Age"].fillna(clean["Age"].median())
clean["Gender"] = clean["Gender"].fillna("Unknown")
clean.to_csv(OUT/"retail_sales_cleaned.csv", index=False)

# Text report
total_revenue = df["Total Amount"].sum()
avg_order = df["Total Amount"].mean()
best_category = category_sales.iloc[0]["Product Category"]
best_product = top_products.iloc[0]["Product"]
report = f"""RETAIL SALES EDA - AUTOMATED SUMMARY

Dataset rows: {len(df)}
Columns: {len(df.columns)}
Total revenue: {total_revenue:,.2f}
Average transaction value: {avg_order:,.2f}
Missing values: {int(df.isnull().sum().sum())}
Highest-revenue category: {best_category}
Most-sold product by quantity: {best_product}

Actionable recommendations (validate with real business context):
1. Prioritise inventory planning for the highest-revenue category and most frequently purchased products.
2. Compare monthly and quarterly peaks with promotions, holidays and stock availability before planning campaigns.
3. Tailor customer campaigns by age group and gender only where sample sizes are adequate and the strategy is appropriate.
4. Monitor average transaction value and test bundles or cross-sells to increase basket size.
5. Improve customer and demographic data capture to reduce missing values and strengthen future analysis.
"""
(OUT/"eda_summary.txt").write_text(report, encoding="utf-8")
print("\\nAnalysis complete. Charts and reports saved in the outputs folder.")
print(report)
