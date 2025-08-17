# scripts/generate_sample_sales.py
import pandas as pd
import numpy as np
from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)
np.random.seed(42)

n = 1000
dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
dates = np.random.choice(dates, size=n)

regions = ["North", "South", "East", "West"]
products = ["A", "B", "C", "D", "E"]
price_map = {"A": 100, "B": 150, "C": 80, "D": 200, "E": 50}
categories = {"A":"Electronics","B":"Electronics","C":"Clothing","D":"Furniture","E":"Accessories"}

prod = np.random.choice(products, size=n)
region = np.random.choice(regions, size=n)
units = np.random.randint(1, 20, size=n)
price = [price_map[p] * np.random.uniform(0.85, 1.25) for p in prod]
sales = (units * np.array(price) + np.random.normal(0, 10, n)).round(2)

df = pd.DataFrame({
    "date": dates,
    "region": region,
    "product": prod,
    "category": [categories[p] for p in prod],
    "units": units,
    "sales": sales
})
df = df.sort_values("date").reset_index(drop=True)
df.to_csv("data/sales_data.csv", index=False)
print("Saved sample data to data/sales_data.csv")