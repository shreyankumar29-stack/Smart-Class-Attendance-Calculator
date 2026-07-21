import streamlit as st
import pandas as pd
import requests
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

st.title("📈 Analytics")

st.caption("Visualize and analyze your attendance performance.")

st.divider()
# =====================================
# FETCH ANALYTICS
# =====================================

response = requests.get(

    "http://127.0.0.1:5000/api/analytics",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

analytics = response.json()

# =====================================
# SUMMARY METRICS
# =====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "📚 Subjects",

        analytics["total_subjects"]

    )

with col2:

    st.metric(

        "📈 Overall Attendance",

        f'{analytics["overall_attendance"]}%'

    )

with col3:

    st.metric(

        "🎯 Target",

        "75%"

    )
# =====================================
# PROGRESS
# =====================================

st.divider()

st.subheader("📊 Overall Attendance Progress")

attendance = analytics["overall_attendance"]

st.progress(attendance / 100)

st.write(f"### {attendance}%")

# =====================================
# PIE CHART
# =====================================

st.divider()

st.subheader("🥧 Present vs Absent")

pie_data = pd.DataFrame({

    "Status": [

        "Present",
        "Absent"

    ],

    "Classes": [

        analytics["present_classes"],

        analytics["absent_classes"]

    ]

})
fig = px.pie(

    pie_data,

    names="Status",

    values="Classes",

    hole=0.45

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# WEEKLY TREND
# =====================================

st.divider()

st.subheader("📈 Weekly Attendance Trend")

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

# =====================================
# SUBJECT PERFORMANCE
# =====================================

st.divider()

st.subheader("📚 Subject Performance")

performance = pd.DataFrame(

    analytics["subject_wise"]

)

performance.rename(

    columns={

        "subject": "Subject",

        "attendance": "Attendance"

    },

    inplace=True

)

st.bar_chart(

    performance,

    x="Subject",

    y="Attendance"

)
# =====================================
# INSIGHTS
# =====================================

st.divider()

st.subheader("💡 Insights")

st.success(

    f"🏆 Best Performing Subject(s):\n\n"

    f"{', '.join(analytics['best_subjects'])}"

    f"\n\nAttendance: {analytics['best_percentage']}%"

)
st.warning(

    f"⚠️ Subject(s) Needing Improvement:\n\n"

    f"{', '.join(analytics['worst_subjects'])}"

    f"\n\nAttendance: {analytics['worst_percentage']}%"

)

if analytics["overall_attendance"] >= 75:

    st.info(

        "🎯 Great! Your overall attendance is above the target."

    )

else:

    st.error(

        "🚨 Your overall attendance is below the target. Attend more classes."

    )

# =====================================
# BEST & WORST SUBJECT
# =====================================

st.divider()

st.subheader("🏆 Performance Overview")

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "🥇 Best Subject",

        ", ".join(analytics["best_subjects"]),

        f'{analytics["best_percentage"]}%'

    )
with col2:

    st.metric(

        "⚠️ Lowest Subject",

        ", ".join(analytics["worst_subjects"]),

        f'{analytics["worst_percentage"]}%'

    )