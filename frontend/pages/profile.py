import streamlit as st
import requests

# =====================================
# LOGIN CHECK
# =====================================

if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.switch_page("pages/Login.py")

# =====================================
# FETCH PROFILE
# =====================================

profile_response = requests.get(

    "http://127.0.0.1:5000/api/profile",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

profile = profile_response.json()

# =====================================
# FETCH ANALYTICS
# =====================================

analytics_response = requests.get(

    "http://127.0.0.1:5000/api/analytics",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

analytics = analytics_response.json()

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

    image_name = profile.get("image_file")

    if not image_name:

        image_name = "default.jpg"

    image_url = (

        "http://127.0.0.1:5000/static/profile_pictures/"

        + image_name

    )

    st.image(

        image_url,

        width=150

    )

    uploaded_image = st.file_uploader(

        "Choose Profile Picture",

        type=[

            "png",

            "jpg",

            "jpeg"

        ]

    )

    if uploaded_image is not None:

        st.image(

            uploaded_image,

            caption="Preview",

            width=150

        )

        upload_col, remove_col = st.columns(2)

        with upload_col:

            if st.button(

                "📤 Upload",

                use_container_width=True

            ):

                files = {

                    "image": (

                        uploaded_image.name,

                        uploaded_image,

                        uploaded_image.type

                    )

                }

                response = requests.post(

                    "http://127.0.0.1:5000/api/profile/upload",

                    data={

                        "user_id": profile["id"]

                    },

                    files=files

                )

                if response.status_code == 200:

                    st.success(

                        response.json()["message"]

                    )

                    st.rerun()

                else:

                    st.error(

                        f"Upload Failed ({response.status_code})"

                    )

                    st.code(

                        response.text

                    )

        with remove_col:

            if profile["image_file"] != "default.jpg":

                if st.button(

                    "🗑 Remove",

                    use_container_width=True,

                    type="secondary"

                ):

                    response = requests.post(

                        "http://127.0.0.1:5000/api/profile/remove",

                        json={

                            "user_id": profile["id"]

                        }

                    )

                    if response.status_code == 200:

                        st.success(

                            response.json()["message"]

                        )

                        st.rerun()

                    else:

                        st.error(

                            response.json()["message"]

                        )

            else:

                st.button(

                    "🗑 Remove",

                    disabled=True,

                    use_container_width=True,

                    type="secondary"

                )

with col2:

    st.subheader(

        profile["username"]

    )

    st.write(

        f"📧 {profile['email']}"

    )

    st.write(

        f"🆔 User ID : {profile['id']}"

    )

    st.write(

        "🎓 Smart Attendance Planner User"

    )

# =====================================
# ACCOUNT STATISTICS
# =====================================

st.divider()

st.subheader("📊 Account Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "📚 Subjects",

        analytics["total_subjects"]

    )

with col2:

    st.metric(

        "📈 Attendance",

        f"{analytics['overall_attendance']}%"

    )

with col3:

    st.metric(

        "🟢 Safe Subjects",

        analytics["safe_subjects"]

    )

with col4:

    st.metric(

        "⚠️ Warning Subjects",

        analytics["warning_subjects"]

    )

# =====================================
# ACCOUNT SETTINGS
# =====================================

st.divider()

st.subheader("⚙️ Account Settings")

col1, col2 = st.columns(2)

with col1:

    if st.button(

    "🔒 Change Password",

    use_container_width=True

):

        st.session_state["show_change_password"] = True

    if st.session_state.get("show_change_password", False):

        st.divider()

        st.subheader("🔒 Change Password")

        current_password = st.text_input(

        "Current Password",

        type="password",

        key="current_password"

    )

    new_password = st.text_input(

        "New Password",

        type="password",

        key="new_password"

    )

    confirm_password = st.text_input(

        "Confirm New Password",

        type="password",

        key="confirm_password"

    )

    if st.button(

        "✅ Update Password",

        use_container_width=True

    ):

        response = requests.post(

            "http://127.0.0.1:5000/api/profile/change-password",

            json={

                "user_id": profile["id"],

                "current_password": current_password,

                "new_password": new_password,

                "confirm_password": confirm_password

            }

        )

        data = response.json()

        if response.status_code == 200:

            st.success(

                data["message"]

            )

            st.session_state["show_change_password"] = False

        else:

            st.error(

                data["message"]

            )

with col2:

    if st.button(

    "🚪 Logout",

    use_container_width=True,

    type="secondary"

):

        st.session_state.clear()

        st.switch_page("pages/Login.py")
# =====================================
# ABOUT
# =====================================

st.divider()

st.subheader("ℹ️ About")

st.info(
"""
Smart Attendance Planner

Version : 1.0

Developed using:
• Streamlit
• Flask
• PostgreSQL
• Python
"""

)