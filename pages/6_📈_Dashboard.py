import streamlit as st
import pandas as pd
from utils.sheets import (
    get_sales_sheet,
    get_student_data_sheet,
    get_attendance_sheet
)
from utils.auth import restrict_access

restrict_access(["Head"])
st.set_page_config(page_title="📈 Dashboard", page_icon="📊")

st.title("📊 Head Dashboard - Student & EM Insights")

# === Load data ===
spreadsheet_id = "1J5sw6MsChe_Fdhz76oR-JH8ljNqXPVLkb-JyVF-3_Qg"

sales_df = get_sales_sheet()
student_df = get_student_data_sheet()


# === Assigned Students Count ===
st.subheader("👥 Students Assigned to EMs")
if "EM Name" in sales_df.columns:
    em_counts = sales_df["EM Name"].value_counts().reset_index()
    em_counts.columns = ["EM Name", "Total Assigned"]
    st.dataframe(em_counts)
else:
    st.warning("Missing 'EM Name' column in salesData.")

# === Admitted vs Pending ===
st.subheader("📌 Student Status")
if "Candidate ID" in sales_df.columns:
    admitted = sales_df[sales_df["Candidate ID"].str.strip() != ""]
    pending = sales_df[sales_df["Candidate ID"].str.strip() == ""]
    col1, col2 = st.columns(2)
    col1.metric("✅ Admitted", len(admitted))
    col2.metric("❌ Pending", len(pending))
else:
    st.warning("Missing 'Candidate ID' column.")

# === Attendance / Class Log Summary ===
