
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Abaday Dashboard Preview", layout="wide")
st.title("Abaday Mid-Stage Preview")

abaday_df = pd.read_csv("abaday_dashboard_data.csv")
collectr_df = pd.read_csv("collectr-data-fixed.csv")

df = pd.concat([abaday_df, collectr_df], ignore_index=True)
df.fillna("", inplace=True)

st.markdown("### Filter Controls")
col1, col2 = st.columns(2)
with col1:
    source_filter = st.selectbox("Source", options=["All"] + sorted(df["Source"].unique()))
with col2:
    owned_filter = st.selectbox("Owned", options=["All", "Yes", "Wishlist"])

if source_filter != "All":
    df = df[df["Source"] == source_filter]
if owned_filter != "All":
    df = df[df["Owned"] == owned_filter]

st.markdown("### Cards")
for _, row in df.iterrows():
    st.markdown(f"**{row['Name']}** | Set: {row['Set']} | Rarity: {row['Rarity']}")
    st.write(f"Price: ${row['Market Price']} | ROI: {row['Profit/Loss (%)']}%")
    st.markdown(f"[TCGplayer]({row['TCGplayer URL']}) | [eBay]({row['eBay URL']})")
    st.markdown("---")
