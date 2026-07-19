import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE TITLE
# =====================================

st.title("📈 Analytics")

st.caption("Visualize and analyze your attendance performance.")

st.divider()

# =====================================
# SUMMARY METRICS
# =====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📚 Subjects",
        6
    )

with col2:

    st.metric(
        "📈 Overall Attendance",
        "82%"
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

attendance = 82

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

        82,
        18

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

performance = pd.DataFrame({

    "Subject": [

        "DBMS",
        "DSA",
        "Python",
        "OS",
        "CN",
        "DM"

    ],

    "Attendance": [

        86,
        72,
        91,
        78,
        83,
        84

    ]

})

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
    "🏆 Best Performing Subject: Python Programming (91%)"
)

st.warning(
    "⚠ Subject Needing Improvement: Data Structures (72%)"
)

st.info(
    "🎯 Maintain attendance above 75% to stay on track."
)