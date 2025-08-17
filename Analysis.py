# scripts/analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("outputs").mkdir(parents=True, exist_ok=True)

df = pd.read_csv("data/cleaned_sales.csv", parse_dates=["date"])

# KPIs
total_sales = df["sales"].sum()
total_units = df["units"].sum()
avg_order_value = total_sales / max(1, len(df))

print(f"Total sales: {total_sales:.2f}")
print(f"Total units: {total_units}")
print(f"Avg order value: {avg_order_value:.2f}")

# Monthly sales
monthly = df.set_index("date").resample("M")["sales"].sum()
plt.figure(figsize=(8,4))
monthly.plot()
plt.title("Monthly Sales")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("outputs/monthly_sales.png", dpi=150)
plt.close()

# Sales by region
region = df.groupby("region")["sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(6,4))
region.plot(kind="bar")
plt.title("Sales by Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("outputs/region_sales.png", dpi=150)
plt.close()

# Top products
top_prod = df.groupby("product")["sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(6,4))
top_prod.plot(kind="bar")
plt.title("Sales by Product")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("outputs/top_products.png", dpi=150)
plt.close()

print("Saved charts to outputs/")