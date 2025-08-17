# Streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------
# Generate synthetic sales data
# --------------------------
np.random.seed(42)  # for reproducibility

data = {
    "date": pd.date_range(start="2023-01-01", periods=200, freq="D"),
    "region": np.random.choice(["North", "South", "East", "West"], size=200),
    "product": np.random.choice(["A", "B", "C", "D"], size=200),
    "sales": np.random.randint(100, 1000, size=200)
}

df = pd.DataFrame(data)

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(layout="wide", page_title="Sales Analysis")
st.title("📊 Sales Data Analysis")

# Sidebar filters
st.sidebar.header("Filters")

min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input("Date range", [min_date, max_date])

regions = st.sidebar.multiselect("Region", options=sorted(df["region"].unique()), default=sorted(df["region"].unique()))
products = st.sidebar.multiselect("Product", options=sorted(df["product"].unique()), default=sorted(df["product"].unique()))

# Apply filters
d1, d2 = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
filtered_df = df[(df["date"] >= d1) & (df["date"] <= d2)]
filtered_df = filtered_df[filtered_df["region"].isin(regions)]
filtered_df = filtered_df[filtered_df["product"].isin(products)]

# --------------------------
# Charts
# --------------------------
st.subheader("Sales Over Time")
fig1 = px.line(filtered_df, x="date", y="sales", color="region", title="Sales Trend by Region")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Sales by Product")
fig2 = px.bar(filtered_df.groupby("product")["sales"].sum().reset_index(),
              x="product", y="sales", title="Total Sales by Product")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sales by Region")
fig3 = px.pie(filtered_df, names="region", values="sales", title="Sales Distribution by Region")
st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# Show data
# --------------------------
st.subheader("Filtered Data")
st.dataframe(filtered_df)
