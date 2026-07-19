import streamlit as st
import pandas as pd

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

with st.form("attendance_form"):

    subject = st.selectbox(

        "Select Subject",

        [

            "Database Design",
            "Data Structures",
            "Python Programming",
            "Operating System",
            "Computer Networks",
            "Discrete Mathematics"

        ]

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

        st.success(

            f"{subject} marked as {status}."

        )

# =====================================
# ATTENDANCE HISTORY
# =====================================

st.divider()

st.subheader("📋 Attendance History")

attendance_history = pd.DataFrame({

    "Date": [

        "17 Jul 2026",
        "16 Jul 2026",
        "15 Jul 2026",
        "14 Jul 2026",
        "13 Jul 2026"

    ],

    "Subject": [

        "Database Design",
        "Data Structures",
        "Python Programming",
        "Operating System",
        "Computer Networks"

    ],

    "Status": [

        "✅ Present",
        "❌ Absent",
        "✅ Present",
        "✅ Present",
        "❌ Absent"

    ]

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

st.subheader("📊 Attendance Summary")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "✅ Present",

        18

    )

with col2:

    st.metric(

        "❌ Absent",

        4

    )

with col3:

    st.metric(

        "📈 Attendance",

        "81.8%"

    )