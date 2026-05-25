import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def connect_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["google_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
    return gspread.authorize(creds)

client = connect_gsheets()
spreadsheet_id = "1J5sw6MsChe_Fdhz76oR-JH8ljNqXPVLkb-JyVF-3_Qg"
sheet = client.open_by_key(spreadsheet_id)

def get_login_data():
    return sheet.worksheet("users")      # ← rename tab to "users" in your sheet

def get_sheet(tab_name):                 # ← this is what all pages use
    return sheet.worksheet(tab_name)
