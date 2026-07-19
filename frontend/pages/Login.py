import streamlit as st
import requests

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Login")

st.caption("Sign in to Smart Class Attendance Planner")

with st.form("login_form"):

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    submitted = st.form_submit_button("Login")

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
            import time

            time.sleep(1)

            st.switch_page("pages/dashboard.py")

        else:

            st.error(response.json()["message"])