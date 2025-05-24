
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

# Concatenate datasets
df = pd.concat([abaday_df, collectr_df], ignore_index=True)

# Fix missing columns
for col in ["Owned", "Image URL", "Market Price", "Purchase Price", "Profit/Loss (USD)", "Profit/Loss (%)"]:
    if col not in df.columns:
        df[col] = ""

# Sidebar filters
st.sidebar.header("Filters")
source_filter = st.sidebar.multiselect("Source", df["Source"].unique(), default=df["Source"].unique())
owned_filter = st.sidebar.selectbox("Owned Status", ["All", "Yes", "Wishlist"])
df = df[df["Source"].isin(source_filter)]
if owned_filter != "All":
    df = df[df["Owned"] == owned_filter]

# Summary
st.metric("🃏 Total Cards", len(df))
st.metric("💰 Portfolio Value", f"${pd.to_numeric(df['Market Price'], errors='coerce').sum():,.2f}")
st.metric("📈 Total Profit", f"${pd.to_numeric(df['Profit/Loss (USD)'], errors='coerce').sum():,.2f}")

# Display cards
st.markdown("### Card Viewer")
for _, row in df.iterrows():
    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            if pd.notna(row.get("Image URL")) and row["Image URL"]:
                st.image(row["Image URL"], width=140)
            else:
                st.image("https://via.placeholder.com/140x200?text=No+Image", width=140)
        with cols[1]:
            st.subheader(row.get("Name", "Unknown Card"))
            st.write(f"**Set**: {row.get('Set', 'N/A')} | **Rarity**: {row.get('Rarity', 'N/A')}")
            st.write(f"**Franchise**: {row.get('Franchise', 'N/A')} | **Source**: {row.get('Source', 'N/A')}")
            st.write(f"💰 **Market Price**: ${row.get('Market Price', 0)}")
            st.write(f"💸 **Purchase Price**: ${row.get('Purchase Price', 0)}")
            st.write(f"📈 **Profit/Loss**: ${row.get('Profit/Loss (USD)', 0)} | {row.get('Profit/Loss (%)', 0)}%")
            st.write(f"✅ **Owned**: {row.get('Owned', 'N/A')}")
            if pd.notna(row.get("TCGplayer URL")) and "http" in row["TCGplayer URL"]:
                st.markdown(f"[🔗 TCGplayer Link]({row['TCGplayer URL']})", unsafe_allow_html=True)
            if pd.notna(row.get("eBay URL")) and "http" in row["eBay URL"]:
                st.markdown(f"[🛒 eBay Listing]({row['eBay URL']})", unsafe_allow_html=True)
