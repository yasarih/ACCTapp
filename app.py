import streamlit as st
import pandas as pd
from utils.sheets import get_login_data

st.set_page_config(page_title="🔐 Login", page_icon="🔐")

# Load login data
login_sheet = get_login_data()
data = login_sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])  # skip header

# Already logged in
if st.session_state.get("logged_in"):
    st.title("📚 Angle Belearn Teacher Portal")
    st.success(f"✅ Logged in as {st.session_state['user']} ({st.session_state['role']})")

    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You have been logged out.")
        st.rerun()

    st.write("Use the sidebar to navigate.")

# Not logged in
else:
    st.title("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        match = df[(df["Name"] == username) & (df["Password"] == password)]
        if not match.empty:
            st.session_state["user"] = username
            st.session_state["role"] = match.iloc[0]["Role"]
            st.session_state["logged_in"] = True
            st.success(f"✅ Logged in as {username} ({st.session_state['role']})")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")
