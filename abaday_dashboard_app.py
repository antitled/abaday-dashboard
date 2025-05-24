
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Abaday Dashboard", layout="wide")
st.title("💼 Abaday Card Portfolio")

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

st.sidebar.header("Filters")
source_filter = st.sidebar.multiselect("Source", df["Source"].unique(), default=df["Source"].unique())
owned_filter = st.sidebar.selectbox("Ownership", ["All", "Yes", "Wishlist"])
df = df[df["Source"].isin(source_filter)]
if owned_filter != "All":
    df = df[df["Owned"] == owned_filter]

st.metric("Total Cards", len(df))
st.metric("Estimated Value", f"${df['Market Price'].sum():,.2f}")
st.metric("Total Profit", f"${df['Profit/Loss (USD)'].sum():,.2f}")

st.markdown("### 📋 Card Details")
for _, row in df.iterrows():
    with st.container():
        cols = st.columns([1, 2, 2])
        with cols[0]:
            if pd.notna(row.get("Image URL")) and row.get("Image URL") != "":
                st.image(row["Image URL"], width=150)
            else:
                st.write("📷 No Image")
        with cols[1]:
            st.subheader(row["Name"])
            st.write(f"**Set**: {row.get('Set', 'N/A')}")
            st.write(f"**Rarity**: {row.get('Rarity', 'N/A')}")
            st.write(f"**Franchise**: {row.get('Franchise', 'N/A')}")
            st.write(f"**Owned**: {row.get('Owned', 'N/A')}")
            st.write(f"**Source**: {row.get('Source', 'N/A')}")
        with cols[2]:
            st.write(f"💰 **Market Price**: ${row.get('Market Price', 0):,.2f}")
            st.write(f"💸 **Purchase Price**: ${row.get('Purchase Price', 0):,.2f}")
            st.write(f"📈 **Profit/Loss**: ${row.get('Profit/Loss (USD)', 0):,.2f}")
            st.write(f"📊 **Change**: {row.get('Profit/Loss (%)', 0)}%")
            if pd.notna(row.get("TCGplayer URL")):
                st.markdown(f"[🔗 TCGplayer]({row['TCGplayer URL']})")
            if pd.notna(row.get("eBay URL")):
                st.markdown(f"[🛒 eBay]({row['eBay URL']})")
