import streamlit as st

def restrict_access(allowed_roles):
    role = st.session_state.get("role", "")
    if role not in allowed_roles:
        st.error("🚫 Unauthorized access")
        st.stop()