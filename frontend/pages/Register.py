import time
import streamlit as st
import requests

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Register",

    page_icon="📝",

    layout="centered"

)

# =====================================
# PAGE TITLE
# =====================================

st.title("📝 Register")

st.caption("Create your Smart Attendance Planner account.")

# =====================================
# REGISTER FORM
# =====================================

with st.form("register_form"):

    username = st.text_input(

        "Username"

    )

    email = st.text_input(

        "Email"

    )

    password = st.text_input(

        "Password",

        type="password"

    )

    confirm_password = st.text_input(

        "Confirm Password",

        type="password"

    )

    submitted = st.form_submit_button(

        "Register"

    )

    if submitted:

        # ============================
        # VALIDATIONS
        # ============================

        if password != confirm_password:

            st.error(

                "Passwords do not match."

            )

        elif len(password) < 6:

            st.error(

                "Password must contain at least 6 characters."

            )

        else:

            response = requests.post(

                "http://127.0.0.1:5000/api/register",

                json={

                    "username": username,

                    "email": email,

                    "password": password

                }

            )

            data = response.json()

            if response.status_code == 201:

                st.success(

                    "Registration Successful ✅"

                )

                time.sleep(1.5)

                st.switch_page(

                    "pages/Login.py"

                )

            else:

                st.error(

                    data["message"]

                )

# =====================================
# LOGIN
# =====================================

st.divider()

st.write(

    "Already have an account?"

)

if st.button(

    "🔐 Login",

    use_container_width=True

):

    st.switch_page(

        "pages/Login.py"

    )