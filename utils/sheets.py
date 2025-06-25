import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# ---- Google Sheets Auth Setup ----
def connect_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["google_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
    return gspread.authorize(creds)

# Authorize only once
client = connect_gsheets()
spreadsheet_id = "1J5sw6MsChe_Fdhz76oR-JH8ljNqXPVLkb-JyVF-3_Qg"
sheet = client.open_by_key(spreadsheet_id)

# ---- Sheet Getter Functions ----
def get_sales_sheet():
    return sheet.worksheet("salesData")

def get_masterclass_sales_sheet():
    return sheet.worksheet("10DayCourseSalesData")

def get_student_data_sheet():
    return sheet.worksheet("studentDetails")

def get_teaching_guide_tracker():
    return sheet.worksheet("teachingGuideTracking")

def get_pptracking_sheet():
    return sheet.worksheet("PPTrackingNew")

def get_pptracking_data_sheet():
    return sheet.worksheet("Data of PPTrackingNew")


def get_pptracking_old_sheet():
    return sheet.worksheet("PPTracking")

def get_login_data():
    return sheet.worksheet("forLogIn")

def get_attendance_sheet():
    return sheet.worksheet("dailyAttandanceLog")

def get_material_release_sheet():
    return sheet.worksheet("MaterialRelease")


