import streamlit as st

st.set_page_config(
    page_title="Smart Class Attendance Planner",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Smart Class Attendance Planner")

st.caption("Plan your attendance. Stay above your target.")

st.divider()

st.success("Welcome to Smart Class Attendance Planner!")

st.write("""
Use the sidebar to navigate through the application.

- 📊 Dashboard
- 📚 Subjects
- 📝 Attendance
- 📈 Analytics
- 👤 Profile
""")