
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Abaday Dashboard Preview", layout="wide")
st.title("Abaday Dashboard (Partial Preview)")

abaday_df = pd.read_csv("abaday_dashboard_data.csv")
collectr_df = pd.read_csv("collectr-data-fixed.csv")

abaday_df["Source"] = "Abaday"
collectr_df["Source"] = "Collectr"

abaday_df.rename(columns={
    "Card Name": "Name",
    "Raw Price (USD)": "Market Price",
    "Your Purchase Price": "Purchase Price"
}, inplace=True)

df = pd.concat([abaday_df, collectr_df], ignore_index=True)
df.fillna("", inplace=True)

st.write("Top Filters:")
st.selectbox("Source", options=["All"] + sorted(df["Source"].unique()))
st.selectbox("Owned", options=["All", "Yes", "Wishlist"])

st.write("Cards:")
for _, row in df.iterrows():
    st.markdown(f"### {row.get('Name', 'Unknown')}")
    st.write(f"Set: {row.get('Set', '')}, Rarity: {row.get('Rarity', '')}")
    st.write(f"Market: ${row.get('Market Price', 0)}, Purchase: ${row.get('Purchase Price', 0)}")
    st.write(f"[TCG Link]({row.get('TCGplayer URL', '#')}) | [eBay]({row.get('eBay URL', '#')})")
