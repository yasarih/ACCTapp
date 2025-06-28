import streamlit as st
import pandas as pd
from utils.sheets import (
    get_student_data_sheet,
    get_teaching_guide_tracker,
    get_material_release_sheet,
    get_pptracking_sheet,
    get_pptracking_data_sheet
)
from utils.auth import restrict_access

# Restrict access to HEAD and DIRECTOR
restrict_access(["Head", "DIRECTOR"])

st.set_page_config(page_title="📊 EM Monitoring Dashboard", page_icon="📊")
st.title("📊 EM-Wise Monitoring Dashboard")

# Load data
student_df = pd.DataFrame(get_student_data_sheet().get_all_records())
guide_df = pd.DataFrame(get_teaching_guide_tracker().get_all_records())
material_df = pd.DataFrame(get_material_release_sheet().get_all_records())
pp_df = pd.DataFrame(get_pptracking_sheet().get_all_records())
ppview = pd.DataFrame(get_pptracking_data_sheet().get_all_records())

# Filter by EM
em_list = sorted(set(guide_df["EM"].dropna().unique().tolist() +
                    material_df["EM"].dropna().unique().tolist() +
                    ppview["EM"].dropna().unique().tolist()))

selected_em = st.selectbox("Select EM to Monitor", em_list)

# Filtered views
guide_view_df = guide_df[guide_df["EM"] == selected_em]
material_view_df = material_df[material_df["EM"] == selected_em]
pp_view_df = ppview[ppview["EM"] == selected_em]

# Show stats
st.markdown(f"## 👤 EM: {selected_em}")
st.markdown("### 🎯 Summary Stats")
st.write(f"Total Assigned Candidates: {guide_view_df['Candidate ID'].nunique()}")
st.write(f"Total Material Records: {material_view_df['Student ID'].nunique()}")
st.write(f"Total PPT Entries: {pp_view_df['Candidate ID'].nunique()}")

# Show Tables
st.markdown("### 📚 Teaching Guide Progress")
if not guide_view_df.empty:
    st.dataframe(guide_view_df, use_container_width=True)
else:
    st.info("No Teaching Guide data available for this EM.")

st.markdown("### 📦 Material Distribution")
if not material_view_df.empty:
    st.dataframe(material_view_df, use_container_width=True)
else:
    st.info("No Material data available for this EM.")

st.markdown("### 🧑‍🏫 PPT Tracking")
if not pp_view_df.empty:
    st.dataframe(pp_view_df, use_container_width=True)
else:
    st.info("No PPT Tracking data available for this EM.")
