import streamlit as st
import pandas as pd
import re
from utils.sheets import get_sales_sheet
from utils.auth import restrict_access

restrict_access(["Head"])
st.set_page_config(page_title="Assign Students", page_icon="📝")

# --- Load sheet and data ---
sales_sheet = get_sales_sheet()
sales_values = sales_sheet.get_all_values()
sales_df = pd.DataFrame(sales_values[1:], columns=sales_values[0])  # skip header row

st.title("📝 Assign EM to Students")

# --- Check required columns ---
if "EM Name" not in sales_df.columns or "Candidate ID" not in sales_df.columns:
    st.error("🛑 Required columns 'EM Name' or 'Candidate ID' missing.")
    st.stop()

# --- Find unassigned students ---
unassigned = sales_df[sales_df["EM Name"].str.strip() == ""]
if unassigned.empty:
    st.info("✅ All students are assigned.")
    st.stop()

unassigned["Row #"] = unassigned.index + 2  # +2 to match Google Sheet row index
st.dataframe(unassigned[["Name", "Amount Paid", "Candidate ID", "Row #"]])

# --- EM Assignment Inputs ---
row_to_assign = st.selectbox("Select Row #", unassigned["Row #"])
assigned_em = st.selectbox("Assign EM", ["Anjitha", "Hridya"])

# --- Generate Next ANGTTC ID ---
existing_ids = sales_df["Candidate ID"].dropna().tolist()
numeric_ids = [int(m.group(1)) for sid in existing_ids if (m := re.search(r"ANGTTC(\\d{4})", sid))]
next_id = f"ANGTTC{(max(numeric_ids) + 1) if numeric_ids else 1:04d}"

assigned_id = st.selectbox("Assign ID", [next_id])

# --- Assign Button ---
if st.button("Assign"):
    try:
        sales_sheet.update_cell(row_to_assign, 17, assigned_em)  # Q = 17
        sales_sheet.update_cell(row_to_assign, 18, assigned_id)  # R = 18
        student_name = sales_sheet.cell(row_to_assign, 2).value  # Name column (B = 2)
        st.success(f"✅ Assigned {assigned_em} and ID {assigned_id} to {student_name}")
    except Exception as e:
        st.error(f"❌ Error during update: {e}")
