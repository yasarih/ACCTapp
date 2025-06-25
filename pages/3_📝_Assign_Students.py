import streamlit as st
import pandas as pd
import re
from utils.sheets import get_sales_sheet
from utils.auth import restrict_access

restrict_access(["Head"])
st.set_page_config(page_title="Assign Students", page_icon="📝")

# --- Load sheet and data ---
sales_sheet = get_sales_sheet()
sales_values = sales_sheet.get_all_values()
sales_df = pd.DataFrame(sales_values[1:], columns=sales_values[0])  # skip header row

st.title("📝 Updating... you might now add using a Google Sheet directly.")

