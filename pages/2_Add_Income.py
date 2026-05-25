import streamlit as st
from utils.sheets import get_sheet
from datetime import date

st.set_page_config(page_title="Add Income", page_icon="➕")

if not st.session_state.get("logged_in"):
    st.warning("⚠️ Please login first.")
    st.stop()

st.title("➕ Record Income")
sheet = get_sheet("income")

with st.form("income_form"):
    dept   = st.selectbox("Department", ["Masjid", "Durus"])
    itype  = st.selectbox("Type", ["Cash", "Bank Transfer", "Gold", "In-Kind"])
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    donor  = st.text_input("Donor Name (optional)")
    notes  = st.text_area("Notes (optional)")
    dt     = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("💾 Save Income", use_container_width=True)

if submitted:
    if amount <= 0:
        st.error("❌ Amount must be greater than zero.")
    else:
        sheet.append_row([
            str(dt),
            st.session_state["user"],
            dept,
            itype,
            amount,
            donor,
            notes,
        ])
        st.success(f"✅ Income of ₹{amount:,.0f} recorded under {dept} ({itype})")
