import streamlit as st
import pandas as pd
import re
from datetime import date
from utils.sheets import get_sales_sheet, get_student_data_sheet, get_new_students_data
from utils.auth import restrict_access

restrict_access(["EM", "DIRECTOR"])
st.set_page_config(page_title="Assign Students", page_icon="📝")

# --- Load sheet and data ---
sales_sheet = get_sales_sheet()
sales_values = sales_sheet.get_all_values()
sales_df = pd.DataFrame(sales_values[1:], columns=sales_values[0])  # skip header row

student_sheet = get_student_data_sheet()
student_values = student_sheet.get_all_values()
student_df = pd.DataFrame(student_values[1:], columns=student_values[0])

new_students_sheet = get_new_students_data()
new_values = new_students_sheet.get_all_values()
new_df = pd.DataFrame(new_values[1:], columns=new_values[0])

em_name = st.session_state.get("user")

st.title("📝 Assign Students")

# Tabs for better separation
tab1, tab2 = st.tabs(["📋 Assigned Students", "➕ New Students"])

with tab1:
    st.subheader("📋 Your Assigned Students")
    if "EM_Name" in student_df.columns:
        filtered_students = student_df[student_df["EM_Name"] == em_name]

        # Batch filter
        batch_list = filtered_students["Batch"].dropna().unique().tolist() if "Batch" in filtered_students.columns else []
        selected_batch = st.selectbox("Filter by Batch", ["All"] + batch_list)
        if selected_batch != "All":
            filtered_students = filtered_students[filtered_students["Batch"] == selected_batch]

        st.dataframe(filtered_students)
    if "EM_Name" in student_df.columns:
        filtered_students = student_df[student_df["EM_Name"] == em_name]
        st.dataframe(filtered_students)
    else:
        st.warning("EM_Name column missing in student data.")

with tab2:
    st.subheader("➕ Your New Students Not Yet Added")
    if "Candidate ID" in new_df.columns and "EM" in new_df.columns:
        existing_ids = student_df["Candidate ID"].dropna().tolist() if "Candidate ID" in student_df.columns else []
        new_entries = new_df[(~new_df["Candidate ID"].isin(existing_ids)) & (new_df["EM"] == em_name)]

        if not new_entries.empty:
            st.dataframe(new_entries)
        else:
            st.info("No new students found for your EM name.")
    else:
        st.warning("Required columns missing in new student data.")

    # Add New Student Form
    st.divider()
    st.subheader("➕ Add New Student")
    with st.form("add_new_student_form"):
        # Lookup from sales_df
        sales_lookup_df = sales_df[["Candidate ID", "Name", "Contact[WhatsApp no]", "Email ID"]].copy() if all(col in sales_df.columns for col in ["Candidate ID", "Name", "Contact[WhatsApp no]", "Email ID"]) else pd.DataFrame()

        # Candidate ID input
        candidate_id = st.text_input("Candidate ID")

        # Autofill details if available
        if candidate_id and not sales_lookup_df.empty:
            match = sales_lookup_df[sales_lookup_df["Candidate ID"] == candidate_id]
            if not match.empty:
                st.session_state["candidate_name"] = match.iloc[0]["Name"]
                st.session_state["contact"] = match.iloc[0]["Contact[WhatsApp no]"]
                st.session_state["login"] = match.iloc[0]["Email ID"]
        today_date = date.today().strftime("%d/%m/%Y")
        candidate_id = st.text_input("Candidate ID")
        candidate_name = st.text_input("Candidate Name", value=st.session_state.get("candidate_name", ""))
        contact = st.text_input("Contact Number", value=st.session_state.get("contact", ""))
        login = st.text_input("Login Credential", value=st.session_state.get("login", ""))
        batch = st.selectbox("Batch", ["BATCH1", "BATCH2", "MTC1"])
        admission_type = st.selectbox("Type Of Admission", ["Platinum", "Gold", "Silver"])
        first_call = st.selectbox("First Call", ["Done", "Pending"])
        connection_mode = st.selectbox("Connection Mode", ["WhatsApp", "Phone", "Email"])
        first_msg = st.selectbox("First Msg From EM Team - WhatsApp", ["Sent", "Not Sent"])
        welcome_mail = st.selectbox("Welcome Mail/ Confirmation mail", ["Sent", "Not Sent"])
        onboarding_schedule = st.selectbox("Onboarding Schedule", ["Scheduled", "Not Scheduled"])
        onboarding_status = st.selectbox("Onboarding Status", ["Completed", "Pending"])
        beginner_guide = st.selectbox("Beginners Guide Status", ["Given", "Not Given"])
        class_updates = st.selectbox("Class Updates", ["Sent", "Pending"])
        diploma_status = st.selectbox("2Month PG Diploma Course Status", ["Ongoing", "Completed", "Not Started"])
        sales_person = st.text_input("Sales Person")
        discount = st.number_input("Discount", min_value=0, value=0)

        submit = st.form_submit_button("Submit")

        if submit:
            new_row = [
                today_date,
                candidate_id,
                candidate_name,
                contact,
                login,
                batch,
                admission_type,
                first_call,
                connection_mode,
                first_msg,
                welcome_mail,
                onboarding_schedule,
                onboarding_status,
                beginner_guide,
                class_updates,
                diploma_status,
                sales_person,
                em_name,
                str(discount)
            ]

            try:
                student_sheet.insert_row(new_row, len(student_values) + 1)
                st.success("Student added successfully!")
                st.rerun()
            except Exception as e:
                st.error("Error while adding student:")
                st.error(str(e))
