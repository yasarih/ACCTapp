import streamlit as st
import pandas as pd
from utils.sheets import get_login_data  # Make sure this exists and works

st.set_page_config(page_title="🔐 Login | Angle Belearn", page_icon="🔐")

# Title
st.title("🔐 Login to Angle Belearn Teacher Portal")

# Load Login Sheet Data
login_sheet = get_login_data()
data = login_sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0]) if data else pd.DataFrame()

# Login State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Login Form
if not st.session_state["logged_in"]:
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
else:
    st.success(f"✅ Welcome back, {st.session_state['user']} ({st.session_state['role']})")
    st.info("Use the sidebar to access different sections.")

    # Logout Button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()