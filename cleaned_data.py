# scripts/clean_data.py
import pandas as pd
from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])
df = df.drop_duplicates().reset_index(drop=True)

# Basic fills for numeric columns
num_cols = df.select_dtypes(include=["number"]).columns
for c in num_cols:
    df[c] = df[c].fillna(df[c].median())

# Fill categorical NA
cat_cols = df.select_dtypes(include=["object"]).columns
for c in cat_cols:
    df[c] = df[c].fillna("Unknown")

# Cap extreme outliers in sales
cap = df["sales"].quantile(0.99)
df["sales"] = df["sales"].clip(upper=cap)

df.to_csv("data/cleaned_sales.csv", index=False)
print("Saved cleaned data to data/cleaned_sales.csv")