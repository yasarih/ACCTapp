import streamlit as st
st.set_page_config(page_title="💘 Class Logbook", page_icon="💘")

import pandas as pd
from utils.sheets import (
    get_student_data_sheet,
    get_teaching_guide_tracker,
    get_pptracking_sheet,
    get_attendance_sheet,
    get_material_release_sheet,
    get_pptracking_data_sheet

)
from utils.auth import restrict_access

# Restrict page access
restrict_access(["EM", "DIRECTOR"])

st.title("💘 Class Logbook")

# Load EM name
em_name = st.session_state.get("user")

# Load data
student_df = pd.DataFrame(get_student_data_sheet().get_all_records())
guide_df = pd.DataFrame(get_teaching_guide_tracker().get_all_records())
material_sheet = get_material_release_sheet()
material_df = pd.DataFrame(material_sheet.get_all_records())
attendance_df = pd.DataFrame(get_attendance_sheet().get_all_records())
pp_df = pd.DataFrame(get_pptracking_sheet().get_all_records())
ppview = pd.DataFrame(get_pptracking_data_sheet().get_all_records())
    


# Filters
guide_view_df = guide_df[guide_df.get("EM") == em_name]
material_view_df = material_df[material_df.get("EM") == em_name]
#attendance_view_df = attendance_df[attendance_df.get("EM") == em_name]
pp_update_df = pp_df[pp_df["EM"] == em_name]
pp_view_df = ppview[ppview["EM"] == em_name]

# Dropdown options
all_options = pd.Series([
    "Timely", "Late", "Perfect", "Ok", "Need Some Improvement", "Bad",
    "Excellent", "Good", "Average", "No/damaged laptop", "Network issues", "Audio issues",
    "Video issues", "More than one issue", "Lighting issue", "Noise issue", "Light and Noise issue",
    "English", "Malayalam", "English and Malayalam", "Not experienced", "Mouse", "Phone/tab",
    "Pentab", "stylis", "Professional", "Unprofessional", "proper way", "Improper way"
])

punctuality_options = all_options[all_options.str.contains("Timely|Late", case=False)].tolist()
intro_options = all_options[all_options.str.contains("Perfect|Improvement|Excellent|Bad|Ok|Good|Need Some Improvement", case=False)].tolist()
tech_options = all_options[all_options.str.contains("Network|Audio|Video|Mouse|Pentab|stylis|Phone", case=False)].tolist()
language_options = all_options[all_options.str.contains("English|Malayalam", case=False)].tolist()
outlook_options = all_options[all_options.str.contains("Professional|Unprofessional", case=False)].tolist()
behavior_options = all_options[all_options.str.contains("proper|improper", case=False)].tolist()

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈EM Dashboard",
    "📚 Teaching Guide Monitoring",
    "📦 Material Release",
    "🗕️ Attendance",
    "📝 Add PP Tracking Data"
])


with tab1:
    st.subheader("📊 EM Dashboard")

    # 🎯 Filter by Batch
    selected_batch = st.selectbox(
        "🎯 Select Batch", ["All"] + sorted(guide_view_df["Batch"].dropna().unique().tolist()),
        key="em_batch_filter"
    )
    if selected_batch != "All":
        guide_view_df = guide_view_df[guide_view_df["Batch"] == selected_batch]
        material_view_df = material_view_df[material_view_df["Batch"] == selected_batch]
        pp_view_df = pp_view_df[pp_view_df["Batch"] == selected_batch]

    # 🧾 Show PPT Tracking Table
    st.markdown("### 🧑‍🏫 PPT Tracking Progress")
    if not pp_view_df.empty:
        st.dataframe(pp_view_df, use_container_width=True)
    else:
        st.info("No PPT tracking data available.")

    # 🧾 Show Guide Progress Table
    st.markdown("### 📚 Teaching Guide Progress")
    guide_display_columns = [
        "Candidate ID", "Candidate Name", "Batch", "EM", "typeOf Community",
        "VideosIn-W1 (12)", "VideosIn-W2 (23)", "VideosIn-W3 (33)", "VideosIn-W4 (45)",
        "VideosIn-W5 (56)", "VideosIn-W6 (69)", "VideosIn-W7 (83)",
        "VideosIn-W8 (90)", "VideosIn-W9 (90)"
    ]
    guide_display_columns = [col for col in guide_display_columns if col in guide_view_df.columns]
    st.dataframe(guide_view_df[guide_display_columns], use_container_width=True)

    # 🧾 Show Material Distribution Table
    st.markdown("### 📦 Material Distribution Progress")
    if not material_view_df.empty:
        st.dataframe(material_view_df, use_container_width=True)
    else:
        st.info("No material distribution data available.")

    # 🔁 Optionally Add Progress Charts or Stats
    st.markdown("### 📈 Summary Stats")
    st.write(f"Total Candidates in Batch: {guide_view_df['Candidate ID'].nunique()}")
    st.write(f"Total Material Records: {material_view_df['Student ID'].nunique()}")

    # You can expand here with metrics, charts or filters as required

with tab2:
    st.subheader("📚 Teaching Guide Monitoring")
    st.markdown("### Teaching Guide Tracker")

    if not guide_view_df.empty:
        # 🎯 Batch Filter
        selected_batch = st.selectbox(
            "🎯 Select Batch", ["All"] + sorted(guide_view_df["Batch"].dropna().unique().tolist())
        )
        if selected_batch != "All":
            guide_view_df = guide_view_df[guide_view_df["Batch"] == selected_batch]

        # 📊 Display Guide Progress Table
        st.subheader("📋 Filtered Guide Progress Table")

        display_columns = [
            "Candidate ID", "Candidate Name", "Batch", "EM", "typeOf Community",
            "VideosIn-W1 (12)", "VideosIn-W2 (23)", "VideosIn-W3 (33)", "VideosIn-W4 (45)",
            "VideosIn-W5 (56)", "VideosIn-W6 (69)", "VideosIn-W7 (83)",
            "VideosIn-W8 (90)", "VideosIn-W9 (90)"
        ]
        available_columns = [col for col in display_columns if col in guide_view_df.columns]

        st.dataframe(guide_view_df[available_columns], use_container_width=True)

        # 📝 Teaching Guide Form (below table)
        st.subheader("📝 Teaching Guide Progress Submission")
        with st.form("🎯 Teaching Progress Form"):
            candidate_id = st.text_input("Candidate ID")
            weekx = st.text_input("Reporting Week")
            guide_feedback = st.text_input("Teaching Guide Feedback / Status")
            submit_guide = st.form_submit_button("Submit")

            if submit_guide and candidate_id and weekx and guide_feedback:
                try:
                    guide_sheet = get_teaching_guide_tracker()
                    data = guide_sheet.get_all_values()

                    # Find or create candidate row
                    candidate_row = None
                    for idx, row in enumerate(data[1:], start=2):
                        if row[0].strip() == candidate_id.strip():
                            candidate_row = idx
                            break

                    if not candidate_row:
                        guide_sheet.append_row([candidate_id])
                        candidate_row = len(data) + 1
                        data.append([candidate_id])

                    # Find column for given week
                    try:
                        week_col = data[0].index(weekx) + 1
                    except ValueError:
                        st.error(f"❌ '{weekx}' not found in header row.")
                        st.stop()

                    # Update the cell
                    guide_sheet.update_cell(candidate_row, week_col, guide_feedback)
                    st.success(f"✅ Updated {candidate_id} for {weekx}.")
                except Exception as e:
                    st.error(f"❌ Update failed: {e}")
    else:
        st.info("No student data found.")
    


with tab3:
    st.subheader("📦 Material Release")

    if not material_view_df.empty:
        # 🎯 Batch Filter
        selected_batch = st.selectbox(
            "🎯 Select Batch", ["All"] + sorted(material_view_df["Batch"].dropna().unique().tolist())
        )

        if selected_batch != "All":
            material_view_df = material_view_df[material_view_df["Batch"] == selected_batch]

        # 📊 Display Guide Progress Table
        st.subheader("📋 Filtered Guide Progress Table")
        st.dataframe(material_view_df, use_container_width=True)

        st.markdown("### ✍️ Submit Completed Material Distribution")

        with st.form("🎯 Material Progress Form"):  # ✅ Unique form key
            candidate_id = st.text_input("Candidate ID")
            released_material = st.text_input("Enter total no. of Materials Released")
            submit_material = st.form_submit_button("Submit")

            if submit_material and candidate_id and released_material:
                try:
                    material_sheet = get_material_release_sheet()
                    data_m = material_sheet.get_all_values()

                    # 🧭 Step 1: Find or create the candidate row
                    candidate_row = None
                    for idx, row in enumerate(data_m[1:], start=2):  # Skip header row
                        if row[0].strip() == candidate_id.strip():
                            candidate_row = idx
                            break

                    if not candidate_row:
                        material_sheet.append_row([candidate_id])
                        candidate_row = len(data_m) + 1
                        data_m.append([candidate_id])  # Extend local copy too

                    # 🧭 Step 2: Find the column index for "EntryFromAPP"
                    try:
                        entry_col = data_m[0].index("EntryFromAPP") + 1  # 1-based indexing
                    except ValueError:
                        st.error("❌ 'EntryFromAPP' column not found in header.")
                        st.stop()

                    # 🧾 Step 3: Update the cell
                    material_sheet.update_cell(candidate_row, entry_col, released_material)
                    st.success(f"✅ Updated 'EntryFromAPP' for {candidate_id}.")

                except Exception as e:
                    st.error(f"❌ Update failed: {e}")
            else:
                st.info("Please provide both Candidate ID and Released Material.")
    

    

with tab4:
    st.subheader("🗕️ Attendance")
    

with tab5:
    
    st.subheader("📝 Add PP Tracking Entry")
    with st.form("pp_entry_form"):
        candidate_id = st.text_input("Candidate ID")
        ppid = st.text_input("PPID")

        inputs = {
            "Punctuality": st.selectbox("Punctuality", punctuality_options),
            "Self Introduction": st.selectbox("Self Introduction", intro_options),
            "Interaction with student": st.selectbox("Interaction with student", intro_options),
            "Technical quality": st.selectbox("Technical quality", tech_options),
            "Background": st.selectbox("Background", outlook_options),
            "Language": st.selectbox("Language", language_options),
            "Communication": st.selectbox("Communication", intro_options),
            "Online writing in whiteboard": st.selectbox("Online writing in whiteboard", intro_options),
            "Network quality (Audio/Video)": st.selectbox("Network quality (Audio/Video)", tech_options),
            "Outlook Of teacher": st.selectbox("Outlook Of teacher", outlook_options),
            "Behavior": st.selectbox("Behavior", behavior_options),
            "Seating arrangement": st.selectbox("Seating arrangement", outlook_options),
            "Confidence level": st.selectbox("Confidence level", intro_options),
            "Subject knowledge": st.selectbox("Subject knowledge", intro_options),
        }

        submit = st.form_submit_button("Submit")

    if submit:
        try:
            new_row = [
                candidate_id,  ppid
            ] + list(inputs.values())
            get_pptracking_sheet().append_row(new_row)
            st.success("✅ PP Tracking data added successfully.")
        except Exception as e:
            st.error(f"❌ Failed to add data: {e}")

