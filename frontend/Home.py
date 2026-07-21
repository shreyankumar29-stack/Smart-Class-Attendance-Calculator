import streamlit as st

st.set_page_config(
    page_title="Smart Class Attendance Calculator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Smart Class Attendance Calculator")

st.caption("Plan your attendance. Stay above your target.")

st.divider()

st.success("Welcome to Smart Class Attendance Calculator!")

st.write("""
Use the sidebar to navigate through the application.

- 📊 Dashboard
- 📚 Subjects
- 📝 Attendance
- 📈 Analytics
- 👤 Profile
""")