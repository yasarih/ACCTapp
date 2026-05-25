import streamlit as st
import pandas as pd
from utils.sheets import get_login_data

st.set_page_config(page_title="🕌 Masjidu Sunnah", page_icon="🕌", layout="wide")

login_sheet = get_login_data()
data = login_sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

if st.session_state.get("logged_in"):
    st.title("🕌 Masjidu Sunnah Finance Portal")
    st.success(f"✅ Logged in as **{st.session_state['user']}** ({st.session_state['role']})")

    st.markdown("---")
    st.subheader("Quick Navigation")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("📊 **Dashboard**\nView totals, balance and charts")
    with col2:
        st.success("➕ **Add Income**\nRecord donations for Masjid or Durus")
    with col3:
        st.error("➖ **Add Expense**\nRecord expenses by category")
    with col4:
        st.warning("📋 **Reports**\nFilter by month or user")

    st.markdown("---")
    st.caption("Use the **sidebar** to navigate between pages.")

    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You have been logged out.")
        st.rerun()

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🕌 Masjidu Sunnah")
        st.subheader("Finance Tracker — Login")
        st.markdown("---")

        with st.form("login_form"):
            username = st.selectbox("👤 Username", ["Ayman", "Hisham", "Thansiq", "Abdullah", "Ihwaan"])  # ← changed
            password = st.text_input("🔑 Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            match = df[(df["Name"] == username) & (df["Password"] == password)]
            if not match.empty:
                st.session_state["user"] = username
                st.session_state["role"] = match.iloc[0]["Role"]
                st.session_state["logged_in"] = True
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
