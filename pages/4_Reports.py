import streamlit as st
import pandas as pd
from utils.sheets import get_sheet

st.set_page_config(page_title="Reports", page_icon="📋", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("⚠️ Please login first.")
    st.stop()

st.title("📋 Reports")

income_df  = pd.DataFrame(get_sheet("income").get_all_records())
expense_df = pd.DataFrame(get_sheet("expenses").get_all_records())

if income_df.empty:
    income_df = pd.DataFrame(columns=["Date","RecordedBy","Department","Type","Amount","Donor","Notes"])
if expense_df.empty:
    expense_df = pd.DataFrame(columns=["Date","RecordedBy","Department","Category","PaidTo","Amount","PaymentMode","Notes"])

income_df["Amount"]  = pd.to_numeric(income_df["Amount"],  errors="coerce").fillna(0)
expense_df["Amount"] = pd.to_numeric(expense_df["Amount"], errors="coerce").fillna(0)
income_df["Month"]   = income_df["Date"].str[:7]
expense_df["Month"]  = expense_df["Date"].str[:7]

# Filters
st.sidebar.header("🔍 Filters")
all_months    = sorted(set(income_df["Month"].tolist() + expense_df["Month"].tolist()), reverse=True)
selected_month = st.sidebar.selectbox("Month", ["All"] + all_months)
selected_dept  = st.sidebar.selectbox("Department", ["All", "Masjid", "Durus"])
selected_user  = st.sidebar.selectbox("User", ["All"] + sorted(income_df["RecordedBy"].unique().tolist()))

def apply_filters(df):
    if selected_month != "All":
        df = df[df["Month"] == selected_month]
    if selected_dept != "All":
        df = df[df["Department"] == selected_dept]
    if selected_user != "All" and "RecordedBy" in df.columns:
        df = df[df["RecordedBy"] == selected_user]
    return df

inc = apply_filters(income_df)
exp = apply_filters(expense_df)

# Summary table
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income",  f"₹{inc['Amount'].sum():,.0f}")
col2.metric("Total Expense", f"₹{exp['Amount'].sum():,.0f}")
col3.metric("Balance",       f"₹{inc['Amount'].sum() - exp['Amount'].sum():,.0f}")

st.markdown("---")

# Monthly breakdown
st.subheader("Monthly Breakdown")
monthly_inc = income_df.groupby("Month")["Amount"].sum().rename("Income")
monthly_exp = expense_df.groupby("Month")["Amount"].sum().rename("Expense")
monthly = pd.concat([monthly_inc, monthly_exp], axis=1).fillna(0)
monthly["Balance"] = monthly["Income"] - monthly["Expense"]
st.dataframe(monthly.sort_index(ascending=False), use_container_width=True)

st.markdown("---")

# Full records with download
tab1, tab2 = st.tabs(["Income Records", "Expense Records"])

with tab1:
    st.dataframe(inc.drop(columns=["Month"], errors="ignore"), use_container_width=True)
    csv = inc.drop(columns=["Month"], errors="ignore").to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Income CSV", csv, "income_report.csv", "text/csv")

with tab2:
    st.dataframe(exp.drop(columns=["Month"], errors="ignore"), use_container_width=True)
    csv = exp.drop(columns=["Month"], errors="ignore").to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Expense CSV", csv, "expense_report.csv", "text/csv")
