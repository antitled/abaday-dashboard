
import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("abaday_dashboard_data.csv")

st.set_page_config(page_title="Abaday Card Portfolio", layout="wide")
st.title("📊 Abaday Card Investment Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
franchise_filter = st.sidebar.multiselect("Franchise", df["Franchise"].unique(), default=df["Franchise"].unique())
ownership_filter = st.sidebar.selectbox("Ownership Status", ["All", "Owned", "Wishlist"])
portfolio_filter = st.sidebar.multiselect("Portfolio Tag", df.get("Portfolio", ["Main"]), default=df.get("Portfolio", ["Main"]))

# Apply filters
filtered_df = df[df["Franchise"].isin(franchise_filter)]
if ownership_filter != "All":
    filtered_df = filtered_df[filtered_df["Owned"] == ownership_filter]
if "Portfolio" in df.columns:
    filtered_df = filtered_df[filtered_df["Portfolio"].isin(portfolio_filter)]

# Dashboard summary
st.metric("📦 Total Cards", len(filtered_df))
st.metric("💰 Portfolio Value", f"${filtered_df['Raw Price (USD)'].sum():,.2f}")
st.metric("📈 Total Profit", f"${filtered_df['Profit/Loss (USD)'].sum():,.2f}")

# Show card table
st.markdown("### Card Table")
st.dataframe(filtered_df, use_container_width=True)

# Show profit/loss chart
st.markdown("### Profit & Loss by Card")
chart_data = filtered_df[["Card Name", "Profit/Loss (USD)"]].set_index("Card Name")
st.bar_chart(chart_data)

# Optional: Show card image links if available
if "Image URL" in df.columns:
    st.markdown("### Card Images")
    for _, row in filtered_df.iterrows():
        st.image(row["Image URL"], caption=row["Card Name"], width=150)
