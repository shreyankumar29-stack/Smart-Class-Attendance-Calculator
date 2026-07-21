import time
import streamlit as st
import requests

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Login",

    page_icon="🔐",

    layout="centered"

)

# =====================================
# PAGE TITLE
# =====================================

st.title("🔐 Login")

st.caption("Sign in to Smart Attendance Planner")

# =====================================
# LOGIN FORM
# =====================================

login_error = None

with st.form("login_form"):

    email = st.text_input(

        "Email"

    )

    password = st.text_input(

        "Password",

        type="password"

    )

    submitted = st.form_submit_button(

        "Login"

    )

    if submitted:

        response = requests.post(

            "http://127.0.0.1:5000/api/login",

            json={

                "email": email,

                "password": password

            }

        )

        if response.status_code == 200:

            data = response.json()

            st.session_state["logged_in"] = True

            st.session_state["user"] = data["user"]

            st.success("Login Successful ✅")

            time.sleep(1)

            st.switch_page("pages/dashboard.py")

        else:

            login_error = response.json()["message"]

# =====================================
# ERROR MESSAGE
# =====================================

if login_error:

    st.error(login_error)

    if login_error == "Invalid Email":

        st.info(

            "Account not found. Please register first."

        )

# =====================================
# REGISTER SECTION
# =====================================

st.divider()

st.write("Don't have an account?")

if st.button(

    "📝 Register Here",

    use_container_width=True

):

    st.switch_page("pages/Register.py")