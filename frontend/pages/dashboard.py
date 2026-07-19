import requests
import streamlit as st
import pandas as pd
import plotly.express as px


# =====================================
# LOGIN CHECK
# =====================================

if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.switch_page("pages/Login.py")



# =====================================
# PAGE TITLE
# =====================================

st.title("📊 Dashboard")

st.write(

    f"Welcome, {st.session_state['user']['username']} 👋"

)

st.divider()


# =====================================
# DASHBOARD DATA
# =====================================
response = requests.get(

    "http://127.0.0.1:5000/api/dashboard",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

data = response.json()


total_subjects = data["total_subjects"]

overall_attendance = data["overall_attendance"]

safe_bunks = data["safe_bunks"]

warning_subjects = data["warning_subjects"]


# =====================================
# METRICS
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Subjects",
        total_subjects
    )

with col2:

    st.metric(
        "📈 Attendance",
        f"{overall_attendance}%"
    )

with col3:

    st.metric(
        "😴 Safe Bunks",
        safe_bunks
    )

with col4:

    st.metric(
        "⚠️ Warnings",
        warning_subjects
    )


# =====================================
# PROGRESS BAR
# =====================================

st.divider()

st.subheader("📈 Overall Attendance Progress")

attendance = overall_attendance

st.progress(
    int(attendance) / 100
)

st.write(f"### {attendance}%")


# =====================================
# STATUS
# =====================================

st.divider()

st.subheader("⚠ Attendance Status")

if warning_subjects == 0:

    st.success(
        "Excellent! Your attendance is above the target."
    )

else:

    st.warning(
        "Some subjects are below the target attendance."
    )


# =====================================
# SUBJECT OVERVIEW (LIVE)
# =====================================

st.divider()

st.subheader("📚 Subject Overview")

response = requests.get(

    "http://127.0.0.1:5000/api/dashboard/subjects",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

subjects = pd.DataFrame(response.json())

st.dataframe(

    subjects,

    hide_index=True,

    use_container_width=True

)

# =====================================
# PIE CHART (Dummy)
# =====================================

st.divider()

st.subheader("🥧 Attendance Distribution")

chart_data = {

    "Status": [

        "Present",
        "Absent"

    ],

    "Classes": [

        82,
        18

    ]

}

fig = px.pie(

    chart_data,

    names="Status",

    values="Classes",

    hole=0.45,

    title="Overall Attendance"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================
# RECENT ACTIVITY (LIVE)
# =====================================

st.divider()

st.subheader("🕒 Recent Attendance Activity")

recent = pd.DataFrame(data["recent_attendance"])

if not recent.empty:

    recent.rename(

        columns={

            "subject_name": "Subject",

            "date": "Date",

            "status": "Status"

        },

        inplace=True

    )

    recent["Status"] = recent["Status"].replace({

        "Present": "✅ Present",

        "Absent": "❌ Absent"

    })

    st.dataframe(

        recent,

        hide_index=True,

        use_container_width=True

    )

else:

    st.info("No attendance records found.")

# =====================================
# ATTENDANCE TREND (Dummy)
# =====================================

st.divider()

st.subheader("📈 Attendance Trend")

trend = pd.DataFrame({

    "Week": [

        "Week 1",
        "Week 2",
        "Week 3",
        "Week 4",
        "Week 5"

    ],

    "Attendance": [

        72,
        75,
        79,
        81,
        82

    ]

})

st.line_chart(

    trend,

    x="Week",

    y="Attendance"

)