import streamlit as st
import pandas as pd
import re
from datetime import date
import traceback
from utils.sheets import get_sales_sheet, get_student_data_sheet
from utils.auth import restrict_access

# Restrict page access
restrict_access(["EM", "DIRECTOR"])

st.set_page_config(page_title="My Students", page_icon="📋")
st.title("📋 My Assigned Students")

# Load Google Sheets
gsheet = get_student_data_sheet()
sales_sheet = get_sales_sheet()
sales_data = sales_sheet.get_all_values()
sales_df = pd.DataFrame(sales_data[1:], columns=sales_data[0])

em_name = st.session_state.get("user")

# Load student sheet data
sheet_data = gsheet.get_all_values()
headers = [col.strip() for col in sheet_data[0]] if sheet_data else []
data_df = pd.DataFrame(sheet_data[1:], columns=headers) if len(sheet_data) > 1 else pd.DataFrame(columns=headers)
existing_ids = data_df["Candidate ID"].dropna().tolist() if "Candidate ID" in data_df.columns else []

# Generate next ID every time based on current data
id_a = [int(m.group(1)) for sid in existing_ids if (m := re.search(r"ANGTTC(\d{4})", sid))]
id_b = [int(m.group(1)) for sid in existing_ids if (m := re.search(r"ANGMTC(\d{4})", sid))]
next_id_a = f"ANGTTC{(max(id_a)+1 if id_a else 1001):04d}"
next_id_b = f"ANGMTC{(max(id_b)+1 if id_b else 1001):04d}"

# --- Tabs ---
tab1, tab2 = st.tabs(["📋 Assigned Students", "➕ Add Candidate"])

# ===========================
# TAB 1: VIEW + EDIT STUDENTS
# ===========================
with tab1:
    st.subheader("📄 Your Students")
    view_df = data_df[data_df["EM_Name"] == em_name] if "EM_Name" in data_df.columns else pd.DataFrame()
    if not view_df.empty:
        st.dataframe(view_df)
    else:
        st.info("No students found under your name.")

    st.subheader("🔄 Edit Existing Student")
    student_id_input = st.text_input("Enter Candidate ID to Edit")
    if student_id_input:
        match_row = data_df[data_df["Candidate ID"] == student_id_input]
        if not match_row.empty:
            with st.form("edit_form"):
                edit_values = {}
                for col in headers:
                    default_val = match_row.iloc[0][col] if col in match_row.columns else ""
                    if col == "Discount":
                        edit_values[col] = st.number_input(col, value=int(default_val) if default_val else 0)
                    else:
                        edit_values[col] = st.text_input(col, value=default_val)
                if st.form_submit_button("Update"):
                    try:
                        row_index = data_df.index[data_df["Candidate ID"] == student_id_input].tolist()
                        if row_index:
                            new_row = [str(edit_values.get(col, "")) for col in headers]
                            gsheet.update(f'A{row_index[0]+2}:{chr(64+len(headers))}{row_index[0]+2}', [new_row])
                            st.success("✅ Student updated successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error("Failed to update:")
                        st.error(str(e))

    st.subheader("🆕 Newly Assigned Students (No Candidate ID)")
    if "EM Name" in sales_df.columns and "Candidate ID" in sales_df.columns:
        unassigned_df = sales_df[(sales_df["EM Name"] == em_name) & (sales_df["Candidate ID"].str.strip() == "")]
        st.dataframe(unassigned_df)
    else:
        st.warning("Required columns missing in sales data.")

# ===================================
# TAB 2: ADD NEW STUDENT
# ===================================
with tab2:
    st.subheader("🖋️ Add New Candidate")

    # --- Suggestion Section ---
    st.markdown("#### 📅 Suggested Candidate IDs")
    c1, c2 = st.columns(2)
    if c1.button(f"Select {next_id_a}"):
        st.session_state["candidate_id"] = next_id_a
    if c2.button(f"Select {next_id_b}"):
        st.session_state["candidate_id"] = next_id_b

    # --- Newly Assigned Sales Leads ---
    assigned_df = sales_df[(sales_df["EM Name"] == em_name) & (sales_df["Candidate ID"].str.strip() == "")]
    if not assigned_df.empty:
        st.markdown("#### 🔍 Select From Newly Assigned Candidates")
        st.dataframe(assigned_df[["Name", "Contact[WhatsApp no]","Alternate Number" ,"Email ID"]])
        selected_name = st.selectbox("Select Name", assigned_df["Name"].tolist())
        selected_row = assigned_df[assigned_df["Name"] == selected_name].iloc[0]
        st.session_state["name"] = selected_row["Name"]
        st.session_state["phone"] = selected_row.get("Contact[WhatsApp no]", "")
        st.session_state["login"] = selected_row.get("Email ID", "")

    # --- Form Section ---
    with st.form("student_form"):
        name = st.text_input("Name", value=st.session_state.get("name", ""))
        phone = st.text_input("Contact Number", value=st.session_state.get("phone", ""))
        candidate_id = st.text_input("Candidate ID", value=st.session_state.get("candidate_id", ""))
        login = st.text_input("Login Credential", value=st.session_state.get("login", ""))
        date_input = st.date_input("Date", value=date.today()).strftime("%d/%m/%Y")

        # Dummy dropdowns
        batch = st.selectbox("Batch", ["BATCH1", "BATCH2", "MTC1"])
        admission_type = st.selectbox("TypeOfAdmission", ["Platinum", "Gold", "Silver"])
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
        # Build row
        row_data = {
            "Date": date_input,
            "Candidate ID": candidate_id,
            "Name": name,
            "Contact Number": phone,
            "Login Credential": login,
            "Batch": batch,
            "TypeOfAdmission": admission_type,
            "First Call": first_call,
            "Connection Mode": connection_mode,
            "First Msg From EM Team - WhatsApp": first_msg,
            "Welcome Mail/ Confirmation mail": welcome_mail,
            "Onboarding Schedule": onboarding_schedule,
            "Onboarding Status": onboarding_status,
            "Beginners Guide Status": beginner_guide,
            "Class Updates": class_updates,
            "2Month PG Diploma Course Status": diploma_status,
            "Sales Person": sales_person,
            "EM_Name": em_name,
            "Discount": str(discount)
        }

        new_row = [row_data.get(col, "") for col in headers]

        try:
            gsheet.insert_row(new_row, len(sheet_data) + 1)
            # Update sales sheet Candidate ID
            if name in sales_df["Name"].values:
                match_idx = sales_df.index[sales_df["Name"] == name].tolist()
                if match_idx:
                    row_number = match_idx[0] + 2  # +2 accounts for header and 0-based index
                    col_number = sales_df.columns.get_loc("Candidate ID") + 1
                    sales_sheet.update_cell(row_number, col_number, candidate_id)
                    sales_df.at[match_idx[0], "Candidate ID"] = candidate_id  # update local df too

            st.success("✅ Student added and sales sheet updated!")
            st.session_state.clear()
            st.rerun()
        except Exception:
            st.error("Error saving data:")
            st.error(traceback.format_exc())
