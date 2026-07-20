import streamlit as st
import pandas as pd
import requests
from datetime import date
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

            st.success(data["message"])

            st.rerun()

        else:

            st.error(data["message"])
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

    attendance_history["Status"] = attendance_history["Status"].replace({

        "Present": "✅ Present",

        "Absent": "❌ Absent"

    })

# =====================================
# FILTER
# =====================================

filter_option = st.selectbox(

    "Filter Records",

    [

        "All",
        "Present",
        "Absent"

    ]

)

if filter_option == "Present":

    filtered = attendance_history[

        attendance_history["Status"] == "✅ Present"

    ]

elif filter_option == "Absent":

    filtered = attendance_history[

        attendance_history["Status"] == "❌ Absent"

    ]

else:

    filtered = attendance_history

st.dataframe(

    filtered,

    hide_index=True,

    use_container_width=True

)

# =====================================
# SUMMARY
# =====================================

st.divider()
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

st.subheader("📊 Attendance Summary")

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