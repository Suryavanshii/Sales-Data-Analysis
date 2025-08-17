# app/streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Sales Analysis")
st.title("Sales Data Analysis")

df = pd.read_csv("cleaned_sales.csv", parse_dates=["date"])

# Sidebar filters
st.sidebar.header("Filters")
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input("Date range", [min_date, max_date])
regions = st.sidebar.multiselect("Region", options=sorted(df["region"].unique()), default=sorted(df["region"].unique()))
products = st.sidebar.multiselect("Product", options=sorted(df["product"].unique()), default=sorted(df["product"].unique()))

# Apply filters
d1, d2 = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
mask = (df["date"] >= d1) & (df["date"] <= d2) & (df["region"].isin(regions)) & (df["product"].isin(products))
dd = df.loc[mask].copy()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total sales", f"{dd['sales'].sum():.2f}")
col2.metric("Total units", f"{int(dd['units'].sum())}")
col3.metric("Avg order value", f"{(dd['sales'].sum() / max(1, len(dd))):.2f}")

# Charts
monthly = dd.set_index("date").resample("M")["sales"].sum().reset_index()
fig1 = px.line(monthly, x="date", y="sales", title="Monthly Sales (filtered)")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(dd.groupby("region")["sales"].sum().reset_index(), x="region", y="sales", title="Sales by Region")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(dd.groupby("product")["sales"].sum().reset_index().sort_values("sales", ascending=False), x="product", y="sales", title="Top Products")
st.plotly_chart(fig3, use_container_width=True)

st.header("Raw data (preview)")
st.dataframe(dd.sort_values("date", ascending=False).head(200))

csv = dd.to_csv(index=False)

st.download_button("Download filtered CSV", data=csv, file_name="filtered_sales.csv")
