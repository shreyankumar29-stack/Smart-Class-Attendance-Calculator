import streamlit as st
import pandas as pd
import requests
from datetime import date

# =====================================
# SESSION STATE
# =====================================

if "edit_attendance" not in st.session_state:

    st.session_state.edit_attendance = None

if "delete_attendance" not in st.session_state:

    st.session_state.delete_attendance = None


# =====================================
# LOGIN CHECK
# =====================================

if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.switch_page("pages/Login.py")


# =====================================
# PAGE TITLE
# =====================================

st.title("📝 Attendance")

st.caption("Mark and manage your attendance records.")

st.divider()


# =====================================
# MARK ATTENDANCE
# =====================================

st.subheader("➕ Mark Attendance")


# =====================================
# FETCH SUBJECTS
# =====================================

response = requests.get(

    "http://127.0.0.1:5000/api/subjects",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

subjects = response.json()

subject_options = {

    subject["subject_name"]: subject["id"]

    for subject in subjects

}


# =====================================
# ATTENDANCE FORM
# =====================================

with st.form("attendance_form"):

    if not subject_options:

        st.info("Please add at least one subject first.")

        st.stop()

    subject = st.selectbox(

        "Select Subject",

        list(subject_options.keys())

    )

    subject_id = subject_options[subject]

    attendance_date = st.date_input(

        "Attendance Date",

        value=date.today()

    )

    status = st.radio(

        "Attendance Status",

        [

            "Present",

            "Absent"

        ],

        horizontal=True

    )

    submitted = st.form_submit_button(

        "Mark Attendance"

    )

    if submitted:

        with st.spinner("Marking attendance..."):

            response = requests.post(

                "http://127.0.0.1:5000/api/attendance",

                json={

                    "subject_id": subject_id,

                    "attendance_date": str(attendance_date),

                    "status": status

                }

            )

        data = response.json()

        if response.status_code == 201:

            st.toast(data["message"], icon="✅")

            st.rerun()

        else:

            st.toast(data["message"], icon="❌")

# =====================================
# ATTENDANCE HISTORY
# =====================================

st.divider()

st.subheader("📋 Attendance History")


# =====================================
# FETCH ATTENDANCE
# =====================================

response = requests.get(

    "http://127.0.0.1:5000/api/attendance",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

attendance_history = pd.DataFrame(response.json())


if not attendance_history.empty:

    attendance_history.rename(

        columns={

            "attendance_date": "Date",

            "subject_name": "Subject",

            "status": "Status"

        },

        inplace=True

    )

    attendance_history["Status"] = attendance_history["Status"].replace(

        {

            "Present": "✅ Present",

            "Absent": "❌ Absent"

        }

    )


# =====================================
# FILTER
# =====================================

filter_option = st.selectbox(

    "Filter Records",

    [

        "All",

        "✅ Present",

        "❌ Absent"

    ]

)

if filter_option == "✅ Present":

    filtered = attendance_history[

        attendance_history["Status"] == "✅ Present"

    ]

elif filter_option == "❌ Absent":

    filtered = attendance_history[

        attendance_history["Status"] == "❌ Absent"

    ]

else:

    filtered = attendance_history


# =====================================
# ATTENDANCE TABLE
# =====================================

if filtered.empty:

    st.info("No attendance records found.")

else:

    header = st.columns([2, 4, 2, 1, 1])

    header[0].markdown("**Date**")
    header[1].markdown("**Subject**")
    header[2].markdown("**Status**")
    header[3].markdown("**Edit**")
    header[4].markdown("**Delete**")

    for _, row in filtered.iterrows():

        col1, col2, col3, col4, col5 = st.columns([2, 4, 2, 1, 1])

        col1.write(row["Date"])

        col2.write(row["Subject"])

        col3.write(row["Status"])

        # ============================
        # EDIT BUTTON
        # ============================

        if col4.button(

            "✏️",

            key=f"edit_attendance_{row['id']}"

        ):

            st.session_state.edit_attendance = row.to_dict()

            st.rerun()

        # ============================
        # DELETE BUTTON
        # ============================

        if col5.button(

            "🗑️",

            key=f"delete_attendance_{row['id']}"

        ):
            st.write("Delete Button clicked")
            st.session_state.delete_attendance = row.to_dict()
            st.write(st.session_state.delete_attendance)
            st.rerun()


# =====================================
# EDIT ATTENDANCE
# =====================================

if st.session_state.edit_attendance is not None:

    st.divider()

    st.subheader("✏️ Edit Attendance")

    with st.form("edit_attendance_form"):

        new_date = st.date_input(

            "Attendance Date",

            value=pd.to_datetime(

                st.session_state.edit_attendance["Date"]

            ).date()

        )

        current_status = (

            "Present"

            if st.session_state.edit_attendance["Status"] == "✅ Present"

            else "Absent"

        )

        new_status = st.radio(

            "Attendance Status",

            [

                "Present",

                "Absent"

            ],

            index=0 if current_status == "Present" else 1,

            horizontal=True

        )

        update = st.form_submit_button(

            "Update Attendance"

        )

        if update:

            with st.spinner("Updating attendance..."):

                response = requests.put(

                    f"http://127.0.0.1:5000/api/attendance/{st.session_state.edit_attendance['id']}",

                    json={

                        "attendance_date": str(new_date),

                        "status": new_status

                    }

                )

            data = response.json()

            if response.status_code == 200:

                st.toast(data["message"], icon="✅")

                st.session_state.edit_attendance = None

                st.rerun()

            else:

                st.toast(data["message"], icon="❌")


# =====================================
# DELETE CONFIRMATION
# =====================================

if st.session_state.delete_attendance is not None:

    st.divider()

    st.warning(

        f"Are you sure you want to delete "

        f"**{st.session_state.delete_attendance['Subject']}** "

        f"attendance on "

        f"**{pd.to_datetime(st.session_state.delete_attendance['Date']).strftime('%d %b %Y')}**?"

    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(

            "✅ Yes, Delete",

            use_container_width=True

        ):

            with st.spinner("Deleting attendance..."):

                response = requests.delete(

                    f"http://127.0.0.1:5000/api/attendance/{st.session_state.delete_attendance['id']}"

                )

            data = response.json()

            if response.status_code == 200:

                st.toast(data["message"], icon="🗑️")

                st.session_state.delete_attendance = None

                st.rerun()

            else:

                st.toast(data["message"], icon="❌")

    with col2:

        if st.button(

            "❌ Cancel",

            use_container_width=True

        ):

            st.session_state.delete_attendance = None

            st.rerun()
# =====================================
# SUMMARY
# =====================================

st.divider()

st.subheader("📊 Attendance Summary")


# =====================================
# SUMMARY CALCULATIONS
# =====================================

if attendance_history.empty:

    present = 0
    absent = 0
    attendance_percentage = 0

else:

    present = len(

        attendance_history[
            attendance_history["Status"] == "✅ Present"
        ]

    )

    absent = len(

        attendance_history[
            attendance_history["Status"] == "❌ Absent"
        ]

    )

    total = present + absent

    attendance_percentage = round(

        (present / total) * 100,

        2

    ) if total > 0 else 0


# =====================================
# SUMMARY METRICS
# =====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "✅ Present",

        present

    )

with col2:

    st.metric(

        "❌ Absent",

        absent

    )

with col3:

    st.metric(

        "📈 Attendance",

        f"{attendance_percentage}%"

    )


# =====================================
# RECORD COUNT
# =====================================

st.caption(

    f"📄 Total Attendance Records: {len(attendance_history)}"

)