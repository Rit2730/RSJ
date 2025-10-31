import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Fixed Income Portfolio Dashboard", page_icon="💼", layout="wide")

# -------------------------
# Header
# -------------------------
st.title("💼 Fixed Income Portfolio Dashboard")
st.markdown("""
Welcome to the **Professional Investment Portfolio Dashboard**.  
It visualizes your fixed-income investments, their returns, allocations, and overall performance.
""")

# -------------------------
# Portfolio Data
# -------------------------
data = {
    "Asset Class": [
        "Govt. Bonds",
        "Tax-Free Bonds (NHAI, REC, PFC)",
        "Post Office Monthly Income Scheme (POMIS)",
        "Senior Citizen Savings Scheme (SCSS)"
    ],
    "Risk": ["Very Low", "Very Low", "Very Low", "Very Low"],
    "Reward (%)": [6.5, 6.0, 7.4, 8.2],
    "Time of Investment (yrs)": [8, 12, 5, 5],
    "Percent of Allocation": [15, 10, 10, 25],
    "Purpose": [
        "Safe income, capital security",
        "Tax-efficient income",
        "Regular income",
        "Safe investment"
    ]
}

df = pd.DataFrame(data)

# -------------------------
# Weighted Portfolio Metrics
# -------------------------
df["Weighted Return"] = (df["Reward (%)"] * df["Percent of Allocation"]) / df["Percent of Allocation"].sum()
weighted_avg_return = df["Weighted Return"].sum()

# -------------------------
# Layout
# -------------------------
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📊 Portfolio Data")
    st.dataframe(df, use_container_width=True, height=250)

with col2:
    st.metric(label="📈 Weighted Average Return", value=f"{weighted_avg_return:.2f}%")
    st.metric(label="⚖️ Overall Risk Level", value="Very Low")
    st.metric(label="🎯 Investment Goal", value="Stable & Tax-efficient Income")

st.markdown("---")

# -------------------------
# Charts Section
# -------------------------
st.subheader("📉 Visual Portfolio Insights")

col3, col4 = st.columns(2)

# Pie Chart – Allocation
with col3:
    pie_fig = px.pie(
        df,
        values="Percent of Allocation",
        names="Asset Class",
        title="Portfolio Allocation (%)",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )
    pie_fig.update_traces(textinfo="percent+label", pull=[0.05, 0.05, 0, 0])
    st.plotly_chart(pie_fig, use_container_width=True)

# Bar Chart – Reward Comparison
with col4:
    bar_fig = px.bar(
        df,
        x="Asset Class",
        y="Reward (%)",
        color="Asset Class",
        title="Reward (%) by Asset Class",
        color_discrete_sequence=px.colors.sequential.Mint
    )
    bar_fig.update_layout(showlegend=False)
    st.plotly_chart(bar_fig, use_container_width=True)

# -------------------------
# Insights Section
# -------------------------
st.subheader("📘 Portfolio Insights")
st.markdown(f"""
- The **weighted average return** of the portfolio is **{weighted_avg_return:.2f}%**, indicating consistent low-risk income.  
- The **highest return** is from **Senior Citizen Savings Scheme (8.2%)**, suitable for long-term safe income.  
- The **allocation mix** prioritizes **capital safety (60%)** and **steady income (40%)**.  
- All instruments maintain a **Very Low risk profile**, ideal for conservative investors.
""")

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit | © 2025")

