import streamlit as st
import pandas as pd
from utils.sheets import get_login_data

st.set_page_config(page_title="Login", page_icon="🔐")
st.title("🔐 Login")

# ---- Load Login Data ----
login_sheet = get_login_data()
data = login_sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# ---- Login Form ----
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    match = df[(df["Name"] == username) & (df["Password"] == password)]
    if not match.empty:
        st.session_state["user"] = username
        st.session_state["role"] = match.iloc[0]["Role"]
        st.success(f"✅ Logged in as {username} ({st.session_state['role']})")
        st.switch_page("Home") if "Home" in st.session_state else None
    else:
        st.error("❌ Invalid credentials. Please try again.")
