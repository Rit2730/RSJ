import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# App Configuration
# -------------------------
st.set_page_config(page_title="Advanced Fixed Income Portfolio", page_icon="💼", layout="wide")

# -------------------------
# Title and Intro
# -------------------------
st.title("💼 Advanced Fixed Income Portfolio Dashboard")
st.markdown("""
This interactive dashboard allows you to:
- Upload or edit your **fixed-income investment portfolio**
- **Add assets** manually  
- **Normalize allocations** to 100%  
- Calculate **weighted returns**
- Visualize data through **charts**
""")

# -------------------------
# Default Data
# -------------------------
default_data = {
    "Asset Class": [
        "Govt. Bonds",
        "Tax-Free Bonds (NHAI, REC, PFC)",
        "Post Office Monthly Income Scheme (POMIS)",
        "Senior Citizen Savings Scheme (SCSS)"
    ],
    "Risk": ["Very Low", "Very Low", "Very Low", "Very Low"],
    "Reward (%)": [6.5, 6.0, 7.4, 8.2],
    "Time of Investment (yrs)": [8, 12, 5, 5],
    "Percent of Allocation": [15.0, 10.0, 10.0, 25.0],
    "Purpose": [
        "Safe income, capital security",
        "Tax-efficient income",
        "Regular income",
        "Safe investment"
    ],
}

df = pd.DataFrame(default_data)

# -------------------------
# Sidebar: Controls
# -------------------------
st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("📂 Upload CSV", type=["csv"])
if uploaded_file is not None:
    try:
        user_df = pd.read_csv(uploaded_file)
        required_cols = {"Asset Class", "Reward (%)", "Percent of Allocation"}
        if not required_cols.issubset(set(user_df.columns)):
            st.sidebar.error("CSV must include at least: Asset Class, Reward (%), Percent of Allocation")
        else:
            df = user_df.copy()
            st.sidebar.success("CSV uploaded successfully.")
    except Exception as e:
        st.sidebar.error(f"Error reading CSV: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("➕ Add New Asset")

with st.sidebar.form("add_asset_form", clear_on_submit=True):
    a_name = st.text_input("Asset Class", "New Asset")
    a_risk = st.selectbox("Risk", ["Very Low", "Low", "Medium", "High"], index=0)
    a_reward = st.number_input("Reward (%)", min_value=0.0, step=0.1, value=5.0)
    a_time = st.number_input("Time of Investment (yrs)", min_value=1, step=1, value=5)
    a_alloc = st.number_input("Percent of Allocation (%)", min_value=0.0, step=0.5, value=5.0)
    a_purpose = st.text_input("Purpose", "Safe investment")
    add_submitted = st.form_submit_button("Add Asset")

if add_submitted:
    new_row = {
        "Asset Class": a_name,
        "Risk": a_risk,
        "Reward (%)": a_reward,
        "Time of Investment (yrs)": a_time,
        "Percent of Allocation": a_alloc,
        "Purpose": a_purpose,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.sidebar.success(f"Added new asset: {a_name}")

st.sidebar.markdown("---")
normalize_choice = st.sidebar.radio(
    "If total allocation ≠ 100%", ("Show warning (default)", "Auto-normalize allocations")
)

# -------------------------
# Data Cleaning
# -------------------------
for col in ["Reward (%)", "Percent of Allocation", "Time of Investment (yrs)"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

# -------------------------
# Main Table
# -------------------------
st.subheader("📊 Portfolio Data")
st.dataframe(df.reset_index(drop=True), use_container_width=True)

# -------------------------
# Allocation Summary
# -------------------------
st.subheader("⚖️ Allocation Summary")

total_alloc = df["Percent of Allocation"].sum()
st.write(f"**Total Allocation:** {total_alloc:.2f}%")

if abs(total_alloc - 100.0) > 1e-6:
    if normalize_choice == "Auto-normalize allocations":
        if total_alloc == 0:
            st.error("Cannot normalize — total allocation is 0.")
        else:
            df["Percent of Allocation"] = df["Percent of Allocation"] / total_alloc * 100.0
            st.success("Allocations normalized to 100%.")
            total_alloc = 100.0
    else:
        st.warning("Allocations do not sum to 100%. Adjust or enable auto-normalization in the sidebar.")

# -------------------------
# Weighted Return Calculation
# -------------------------
st.subheader("📈 Portfolio Performance")

if total_alloc > 0:
    weighted_avg_return = (df["Reward (%)"] * df["Percent of Allocation"]).sum() / total_alloc
else:
    weighted_avg_return = 0.0

st.metric(label="Weighted Average Return", value=f"{weighted_avg_return:.2f}%")
st.write("**Overall Risk Level:**", "Very Low" if (df["Risk"] == "Very Low").all() else "Mixed")

df["Weighted Contribution (%)"] = (df["Reward (%)"] * df["Percent of Allocation"]) / 100.0
st.dataframe(df[["Asset Class", "Reward (%)", "Percent of Allocation", "Weighted Contribution (%)"]], use_container_width=True)

# -------------------------
# Charts Section
# -------------------------
st.subheader("📉 Charts")

col1, col2 = st.columns(2)

# Pie chart - allocation
with col1:
    st.markdown("**Allocation Pie Chart**")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    labels = df["Asset Class"]
    sizes = df["Percent of Allocation"]
    if sizes.sum() == 0:
        ax1.text(0.5, 0.5, "No data", ha="center", va="center")
    else:
        ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
    st.pyplot(fig1)

# Bar chart - reward
with col2:
    st.markdown("**Reward (%) by Asset Class**")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.barh(df["Asset Class"], df["Reward (%)"], color="skyblue")
    ax2.set_xlabel("Reward (%)")
    ax2.set_ylabel("Asset Class")
    ax2.set_title("Rewards by Asset")
    st.pyplot(fig2)

# -------------------------
# Insights
# -------------------------
st.subheader("📘 Insights")
st.markdown(f"""
- **Weighted Average Return:** {weighted_avg_return:.2f}%  
- **Total Allocation:** {total_alloc:.2f}%  
- **Total Assets:** {len(df)}  
- **Portfolio Risk Level:** {'Very Low' if (df['Risk'] == 'Very Low').all() else 'Mixed'}  
""")

st.info("💡 Tip: You can upload your own CSV, edit values, and view updated metrics instantly.")

st.markdown("---")
st.caption("Created with ❤️ using Streamlit — fully deployable on Streamlit Cloud without Plotly.")
