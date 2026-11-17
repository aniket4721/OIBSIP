# OIBSIP – Data Analytics – Task 1: EDA on Retail Sales Data

## Project overview
This project performs exploratory data analysis (EDA) on a retail sales dataset. It examines data quality, descriptive statistics, sales trends, customer demographics, product performance and relationships between numeric variables.

**Important:** `dataset/retail_sales.csv` is a synthetic practice dataset generated for this project. It is not real customer or company data. If your internship requires a specific approved dataset, replace it with that dataset and adjust column names in the notebook/script.

## Folder structure
```text
OIBSIP_DataAnalytics_Task1_EDA_RetailSales/
├── dataset/
│   └── retail_sales.csv
├── outputs/                 # generated charts, CSV summaries and report
├── screenshots/             # add your own VS Code/output screenshots here
├── src/
│   └── analyze_retail_sales.py
├── EDA_Retail_Sales.ipynb
├── requirements.txt
└── README.md
```

## Run in VS Code (Windows PowerShell)
1. Open this project folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
4. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
5. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Register the notebook kernel:
   ```powershell
   python -m ipykernel install --user --name=oibsip-env --display-name "Python (OIBSIP)"
   ```
7. Open `EDA_Retail_Sales.ipynb`, select kernel **Python (OIBSIP)**, and run all cells from top to bottom.

## Run the Python script instead
```powershell
python src/analyze_retail_sales.py
```
The script saves charts, summary CSV files, a cleaned dataset and `eda_summary.txt` in `outputs/`.

## Analysis included
- Dataset shape, columns, data types and missing values
- Descriptive statistics
- Monthly and quarterly sales trends
- Age-group and gender breakdown
- Top 10 products by quantity sold
- Revenue by product category
- Numeric correlation heatmap
- Additional revenue-by-gender analysis
- Basic missing-value handling and cleaned CSV export
- Actionable business recommendations

## Before submitting your internship task
- Review every chart and write your own observations based on the actual results.
- Add screenshots of your notebook running successfully to `screenshots/`.
- Update this README with your name, internship track and any dataset source required by your program.
- Add your own demo video and LinkedIn post as required by the internship instructions.
- Follow the official OIBSIP submission instructions and deadline. This project folder is a starter project, not proof of submission or completion.
