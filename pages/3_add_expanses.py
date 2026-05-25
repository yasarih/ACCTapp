import streamlit as st
from utils.sheets import get_sheet
from datetime import date

st.set_page_config(page_title="Add Expense", page_icon="➖")

if not st.session_state.get("logged_in"):
    st.warning("⚠️ Please login first.")
    st.stop()

st.title("➖ Record Expense")
sheet = get_sheet("expenses")

CATEGORIES = {
    "Masjid": ["Electricity", "Water", "Maintenance", "Cleaning", "Imam Salary", "Other"],
    "Durus":  ["Books & Materials", "Speaker Fee", "Venue", "Refreshments", "Other"],
}

dept = st.selectbox("Department", ["Masjid", "Durus"])  # outside form for reactivity

with st.form("expense_form"):
    category     = st.selectbox("Category", CATEGORIES[dept])
    paid_to      = st.text_input("Paid To (person / vendor)")
    amount       = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    payment_mode = st.selectbox("Payment Mode", ["Cash", "Bank Transfer", "UPI"])
    notes        = st.text_area("Notes (optional)")
    dt           = st.date_input("Date", value=date.today())
    submitted    = st.form_submit_button("💾 Save Expense", use_container_width=True)

if submitted:
    if amount <= 0:
        st.error("❌ Amount must be greater than zero.")
    else:
        sheet.append_row([
            str(dt),
            st.session_state["user"],
            dept,
            category,
            paid_to,
            amount,
            payment_mode,
            notes,
        ])
        st.success(f"✅ Expense of ₹{amount:,.0f} recorded under {dept} → {category}")
