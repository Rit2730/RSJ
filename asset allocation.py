import streamlit as st
import pandas as pd

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Investment Portfolio Dashboard", page_icon="💹", layout="wide")

st.title("💹 Advanced Investment Portfolio Dashboard")
st.markdown("""
Analyze and visualize diversified investments across various **risk levels**, 
**returns**, and **time horizons**.  
Use the filters to explore performance insights for different risk categories.
""")

# -------------------------
# Portfolio Data
# -------------------------
data = {
    "Asset Class": [
        "Government Bonds",
        "Tax-Free Bonds (NHAI, REC, PFC)",
        "Post Office Monthly Income Scheme (POMIS)",
        "Senior Citizen Savings Scheme (SCSS)",
        "Corporate Bonds (AAA Rated)",
        "Balanced Mutual Fund",
        "Equity Mutual Fund (Large Cap)",
        "Equity Mutual Fund (Mid Cap)",
        "Gold ETF",
        "REITs"
    ],
    "Risk": [
        "Very Low", "Very Low", "Very Low", "Very Low",
        "Low", "Moderate", "Moderate", "High", "Moderate", "High"
    ],
    "Reward (%)": [6.5, 6.0, 7.4, 8.2, 8.5, 10.5, 12.0, 15.0, 9.0, 13.0],
    "Time of Investment": [
        "3–10 yrs", "10–15 yrs", "5 yrs", "5 yrs",
        "3–7 yrs", "3–5 yrs", "5–7 yrs", "5–10 yrs", "2–5 yrs", "5–10 yrs"
    ],
    "Allocation (%)": [10, 10, 5, 10, 10, 15, 15, 10, 5, 10],
    "Purpose": [
        "Safe income, capital protection",
        "Tax-efficient long-term income",
        "Regular monthly income",
        "Secure income for retirees",
        "Slightly higher return with safety",
        "Balanced growth and income",
        "Stable long-term equity growth",
        "Aggressive growth potential",
        "Hedge against inflation",
        "Real estate-linked income"
    ]
}

df = pd.DataFrame(data)

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("📊 Filter Investments")
selected_risk = st.sidebar.multiselect(
    "Select Risk Level", options=df["Risk"].unique(), default=df["Risk"].unique()
)
selected_purpose = st.sidebar.multiselect(
    "Select Purpose", options=df["Purpose"].unique(), default=[]
)

filtered_df = df[df["Risk"].isin(selected_risk)]
if selected_purpose:
    filtered_df = filtered_df[filtered_df["Purpose"].isin(selected_purpose)]

# -------------------------
# Main Dashboard
# -------------------------
st.subheader("📈 Investment Portfolio Overview")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------
# Charts
# -------------------------
st.subheader("💰 Allocation by Asset Class")

chart_data = filtered_df[["Asset Class", "Allocation (%)"]].set_index("Asset Class")
st.bar_chart(chart_data)

st.subheader("📉 Average Reward by Risk Category")
avg_reward = filtered_df.groupby("Risk")["Reward (%)"].mean().sort_values(ascending=True)
st.bar_chart(avg_reward)

# -------------------------
# Calculations & Insights
# -------------------------
st.subheader("📊 Portfolio Insights")

total_allocation = filtered_df["Allocation (%)"].sum()
avg_return = (filtered_df["Reward (%)"] * filtered_df["Allocation (%)"]).sum() / total_allocation
risk_levels = filtered_df["Risk"].value_counts().to_dict()

st.markdown(f"""
- **Total Allocation:** {total_allocation:.2f}%  
- **Weighted Average Return:** {avg_return:.2f}%  
- **Dominant Risk Category:** {max(risk_levels, key=risk_levels.get)}  
""")

if avg_return < 8:
    st.info("💡 Insight: Your portfolio is conservative with stable but moderate returns.")
elif 8 <= avg_return < 12:
    st.success("🚀 Insight: Your portfolio has a balanced mix of safety and growth.")
else:
    st.warning("⚠️ Insight: Your portfolio is aggressive — expect higher risk and return volatility.")

# -------------------------
# Summary Table by Risk
# -------------------------
st.subheader("📘 Risk Category Summary")
summary = (
    df.groupby("Risk")[["Reward (%)", "Allocation (%)"]]
    .mean()
    .rename(columns={"Reward (%)": "Avg Return (%)", "Allocation (%)": "Avg Allocation (%)"})
    .reset_index()
)
st.dataframe(summary, use_container_width=True)

st.markdown("---")
st.caption("Created with ❤️ using Streamlit | Advanced Portfolio Dashboard")
