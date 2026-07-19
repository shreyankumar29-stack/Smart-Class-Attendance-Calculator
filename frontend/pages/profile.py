import streamlit as st

# =====================================
# PAGE TITLE
# =====================================

st.title("👤 Profile")

st.caption("Manage your account information.")

st.divider()

# =====================================
# PROFILE
# =====================================

col1, col2 = st.columns([1, 3])

with col1:

    st.image(
        "https://api.dicebear.com/7.x/initials/png?seed=Student",
        width=140
    )

with col2:

    st.subheader("Shreyansh")

    st.write("📧 demo@gmail.com")

    st.write("🎓 Computer Science Student")

    st.write("🏫 Lovely Professional University")

# =====================================
# ACCOUNT STATISTICS
# =====================================

st.divider()

st.subheader("📊 Account Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "📚 Subjects",

        6

    )

with col2:

    st.metric(

        "📈 Attendance",

        "82%"

    )

with col3:

    st.metric(

        "😴 Safe Bunks",

        4

    )

with col4:

    st.metric(

        "⚠ Warnings",

        1

    )

# =====================================
# ACCOUNT SETTINGS
# =====================================

st.divider()

st.subheader("⚙ Account Settings")

change_password = st.button(
    "🔒 Change Password"
)

logout = st.button(
    "🚪 Logout"
)

if change_password:

    st.info(
        "Password feature will be connected with Flask backend."
    )

if logout:

    st.success(
        "Logout feature will be connected with Flask backend."
    )

# =====================================
# ABOUT
# =====================================

st.divider()

st.subheader("ℹ About")

st.info(

    """
Smart Class Attendance Planner

Version : 1.0

Developed using:

• Streamlit

• Flask

• PostgreSQL

• Python
    """

)