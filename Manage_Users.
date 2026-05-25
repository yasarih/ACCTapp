import streamlit as st
import pandas as pd
from utils.sheets import get_login_data
from utils.auth import restrict_access

restrict_access(["Head"])

st.set_page_config(page_title="User Manager", page_icon="➕")
st.title("➕ Manage Login Users")

# ---- Load Existing Users ----
login_sheet = get_login_data()
data = login_sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

st.subheader("👥 Current Users")
st.dataframe(df)

# ---- Add New User ----
st.divider()
st.subheader("➕ Add New User")

with st.form("add_user_form"):
    name = st.text_input("Name")
    password = st.text_input("Password")
    role = st.selectbox("Role", ["Head", "EM"])
    submit = st.form_submit_button("Add User")

if submit:
    if name and password and role:
        try:
            login_sheet.append_row([name, password, role])
            st.success(f"✅ User '{name}' added as {role}.")
        except Exception as e:
            st.error(f"❌ Failed to add user: {e}")
    else:
        st.warning("Please fill in all fields.")
