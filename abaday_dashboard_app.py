
import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("abaday_dashboard_data.csv")

st.set_page_config(page_title="Abaday Card Portfolio", layout="wide")

st.title("📊 Abaday Card Investment Dashboard")

# Summary cards
st.metric("📦 Total Cards", len(df))
st.metric("💰 Portfolio Value", f"${df[df['Owned'] == 'Yes']['Raw Price (USD)'].sum():,.2f}")
st.metric("📈 Total Profit", f"${df[df['Owned'] == 'Yes']['Profit/Loss (USD)'].sum():,.2f}")

st.markdown("### Filter by Franchise")
franchise_filter = st.multiselect("Select Franchise(s):", df["Franchise"].unique(), default=df["Franchise"].unique())
filtered_df = df[df["Franchise"].isin(franchise_filter)]

st.markdown("### Filter by Ownership")
owned_filter = st.radio("Owned Status", options=["All", "Yes", "No"])
if owned_filter != "All":
    filtered_df = filtered_df[filtered_df["Owned"] == owned_filter]

st.markdown("### Card Table")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

st.markdown("### Profit & Loss Chart")
chart_data = filtered_df[["Card Name", "Profit/Loss (USD)"]].set_index("Card Name")
st.bar_chart(chart_data)
