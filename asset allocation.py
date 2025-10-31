import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced Fixed Income Portfolio", page_icon="💼", layout="wide")

st.title("💼 Advanced Fixed Income Portfolio Dashboard")
st.markdown(
    "Interactive dashboard for fixed-income allocations. "
    "Upload your CSV, add assets manually, normalize allocations and compute weighted returns."
)

# -------------------------
# Default data (your table)
# -------------------------
default_data = {
    "Asset Class": [
        "Govt. Bonds",
        "Tax-Free Bonds (NHAI, REC, PFC)",
        "Post Office Monthly Income Scheme (POMIS)",
        "Senior Citizen Savings Scheme (SCSS)"
    ],
    "Risk": ["Very Low", "Very Low", "Very Low", "Very Low"],
    "Reward (%)": [6.5, 6.0, 7.4, 8.2],  # numeric
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
# Sidebar controls
# -------------------------
st.sidebar.header("Data Controls")

uploaded_file = st.sidebar.file_uploader("Upload CSV to replace table", type=["csv"])
if uploaded_file is not None:
    try:
        user_df = pd.read_csv(uploaded_file)
        # Basic validation
        required_cols = {"Asset Class", "Reward (%)", "Percent of Allocation"}
        if not required_cols.issubset(set(user_df.columns)):
            st.sidebar.error(
                "CSV must include at least columns: Asset Class, Reward (%), Percent of Allocation"
            )
        else:
            df = user_df.copy()
            st.sidebar.success("CSV loaded successfully.")
    except Exception as e:
        st.sidebar.error(f"Failed to read CSV: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("Add a new asset")
with st.sidebar.form("add_asset_form", clear_on_submit=True):
    a_name = st.text_input("Asset Class", value="New Asset")
    a_risk = st.selectbox("Risk", ["Very Low", "Low", "Medium", "High"], index=0)
    a_reward = st.number_input("Reward (%)", min_value=0.0, step=0.1, value=5.0)
    a_time = st.number_input("Time of Investment (yrs)", min_value=0, step=1, value=5)
    a_alloc = st.number_input("Percent of Allocation (%)", min_value=0.0, step=0.5, value=5.0)
    a_purpose = st.text_input("Purpose", value="")
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
    st.sidebar.success(f"Added asset: {a_name}")

st.sidebar.markdown("---")
normalize_choice = st.sidebar.radio(
    "If total allocation ≠ 100%", ("Show warning (default)", "Auto-normalize allocations")
)

# -------------------------
# Main layout
# -------------------------
st.subheader("📊 Portfolio Data")
st.write(
    "You can upload a CSV in the sidebar or add assets. Expected numeric columns: `Reward (%)`, `Percent of Allocation`."
)

# Convert numeric columns (if uploaded CSV had strings)
for col in ["Reward (%)", "Percent of Allocation", "Time of Investment (yrs)"]:
    if col in df.columns:
        # coerce errors to NaN, then fill with 0 or reasonable defaults
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill NaN with 0 to avoid crashes (and inform user)
if df[["Reward (%)", "Percent of Allocation"]].isnull().any().any():
    st.warning("Some numeric fields had invalid values and were coerced to 0. Please check your data.")
    df[["Reward (%)", "Percent of Allocation"]] = df[["Reward (%)", "Percent of Allocation"]].fillna(0.0)

st.dataframe(df.reset_index(drop=True), use_container_width=True)

# -------------------------
# Allocation checks & normalization
# -------------------------
total_alloc = df["Percent of Allocation"].sum()
st.markdown("---")
st.subheader("⚖️ Allocation Summary")
st.write(f"**Total Allocation:** {total_alloc:.2f}%")

if abs(total_alloc - 100.0) > 1e-6:
    if normalize_choice == "Show warning (default)":
        st.error(
            "Total allocation does not sum to 100%. "
            "Either adjust allocations or select 'Auto-normalize allocations' in the sidebar."
        )
    else:
        # Auto-normalize
        if total_alloc == 0:
            st.error("Total allocation is 0 — cannot normalize. Please add allocations > 0.")
        else:
            df["Percent of Allocation"] = df["Percent of Allocation"] / total_alloc * 100.0
            total_alloc = df["Percent of Allocation"].sum()
            st.success(f"Allocations normalized. New total: {total_alloc:.2f}%")
            st.dataframe(df.reset_index(drop=True), use_container_width=True)

# -------------------------
# Weighted return calculation
# -------------------------
st.markdown("---")
st.subheader("📈 Portfolio Performance")

# Weighted return = sum(reward% * allocation%) / sum(allocation%)
if df["Percent of Allocation"].sum() == 0:
    st.warning("Sum of allocations is 0 — weighted return cannot be computed.")
    weighted_avg_return = 0.0
else:
    weighted_avg_return = (df["Reward (%)"] * df["Percent of Allocation"]).sum() / df["Percent of Allocation"].sum()

st.metric("Weighted Average Return", f"{weighted_avg_return:.2f}%")
st.write("**Overall Risk Level:**", "Very Low" if (df["Risk"] == "Very Low").all() else "Mixed")

# Show weighted contribution column
df["Weighted Contribution (%)"] = (df["Reward (%)"] * df["Percent of Allocation"]) / 100.0
st.write("Weighted contributions (Reward × Allocation / 100):")
st.dataframe(df[["Asset Class", "Reward (%)", "Percent of Allocation", "Weighted Contribution (%)"]], use_container_width=True)

# -------------------------
# Charts (matplotlib)
# -------------------------
st.markdown("---")
st.subheader("📊 Charts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Allocation Pie Chart**")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    labels = df["Asset Class"]
    sizes = df["Percent of Allocation"]
    # if total is zero, show empty chart gracefully
    if sizes.sum() == 0:
        ax1.text(0.5, 0.5, "No allocation data", ha="center", va="center")
    else:
        wedges, texts, autotexts = ax1.pie(
            sizes,
            labels=labels,
            autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
            startangle=90,
            wedgeprops=dict(width=0.5),
        )
        ax1.axis("equal")
    st.pyplot(fig1)

with col2:
    st.markdown("**Reward (%) by Asset (Bar Chart)**")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    x = df["Asset Class"]
    y = df["Reward (%)"]
    ax2.barh(x, y)
    ax2.set_xlabel("Reward (%)")
    ax2.set_title("Reward by Asset Class")
    st.pyplot(fig2)

# -------------------------
# Insights + Export
# -------------------------
st.markdown("---")
st.subheader("📝 Insights")
st.markdown(
    f"- Weighted average return: **{weighted_avg_return:.2f}%**\n"
    f"- Total allocation: **{df['Percent of Allocation'].sum():.2f}%**\n"
    f"- Number of assets: **{len(df)}**\n"
)
st.info("Tip: Export the table (copy/paste) or upload a corrected CSV to replace data.")

st.markdown("---")
st.caption("Created with ❤️ using S
