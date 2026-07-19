import streamlit as st
import pandas as pd
import requests


# =====================================
# LOGIN CHECK
# =====================================

if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.switch_page("pages/Login.py")


# =====================================
# PAGE TITLE
# =====================================

st.title("📚 Subjects")
if "edit_subject" not in st.session_state:
    st.session_state.edit_subject = None

st.caption("Manage all your subjects from one place.")

st.divider()


# =====================================
# ADD SUBJECT
# =====================================

st.subheader("➕ Add New Subject")

with st.form("add_subject_form"):

    subject_name = st.text_input(
        "Subject Name"
    )

    subject_code = st.text_input(
        "Subject Code"
    )

    target = st.slider(
        "Target Attendance (%)",
        min_value=50,
        max_value=100,
        value=75
    )

    submitted = st.form_submit_button(
        "Add Subject"
    )

    if submitted:

        response = requests.post(

            "http://127.0.0.1:5000/api/subjects",

            json={

                "user_id": st.session_state["user"]["id"],

                "subject_name": subject_name,

                "subject_code": subject_code,

                "target": target

            }

        )

        data = response.json()

        if response.status_code == 201:

            st.success(data["message"])

            st.rerun()

        else:

            st.error(data["message"])


st.divider()


# =====================================
# FETCH SUBJECTS
# =====================================

response = requests.get(

    "http://127.0.0.1:5000/api/subjects",

    params={

        "user_id": st.session_state["user"]["id"]

    }

)

subjects = pd.DataFrame(response.json())

subjects.rename(

    columns={

        "subject_name": "Subject",

        "subject_code": "Code",

        "target_percentage": "Target"

    },

    inplace=True

)

subjects["Status"] = "✅ Safe"


# =====================================
# SUBJECTS
# =====================================

st.subheader("📋 Your Subjects")


# =====================================
# SEARCH
# =====================================

search = st.text_input(

    "🔍 Search Subject"

)

if search:

    subjects = subjects[
        subjects["Subject"].str.contains(
            search,
            case=False
        )
    ]


header = st.columns([4,2,2,2,1,1])

header[0].markdown("**Subject**")
header[1].markdown("**Code**")
header[2].markdown("**Target**")
header[3].markdown("**Status**")
header[4].markdown("**Edit**")
header[5].markdown("**Delete**")


for _, row in subjects.iterrows():

    col1, col2, col3, col4, col5, col6 = st.columns([4,2,2,2,1,1])

    col1.write(row["Subject"])
    col2.write(row["Code"])
    col3.write(f'{row["Target"]}%')
    col4.write(row["Status"])

    if col5.button("✏️", key=f"edit_{row['id']}"):

        st.session_state.edit_subject = row.to_dict()

        st.rerun()
    if col6.button("🗑", key=f"delete_{row['id']}"):

        response = requests.delete(

            f"http://127.0.0.1:5000/api/subjects/{row['id']}",

            params={

                "user_id": st.session_state["user"]["id"]

            }

        )

        data = response.json()

        if response.status_code == 200:

            st.success(data["message"])

            st.rerun()

        else:

            st.error(data["message"])
# =====================================
# EDIT SUBJECT
# =====================================

if st.session_state.edit_subject is not None:

    st.divider()

    st.subheader("✏️ Edit Subject")

    with st.form("edit_subject_form"):

        new_name = st.text_input(
            "Subject Name",
            value=st.session_state.edit_subject["Subject"]
        )

        new_code = st.text_input(
            "Subject Code",
            value=st.session_state.edit_subject["Code"]
        )

        new_target = st.slider(
            "Target Attendance (%)",
            50,
            100,
            int(st.session_state.edit_subject["Target"])
        )

        update = st.form_submit_button(
            "Update Subject"
        )

        if update:

            response = requests.put(

                f"http://127.0.0.1:5000/api/subjects/{st.session_state.edit_subject['id']}",

                json={

                    "subject_name": new_name,

                    "subject_code": new_code,

                    "target": new_target

                }

            )

            data = response.json()

            if response.status_code == 200:

                st.success(data["message"])

                st.session_state.edit_subject = None

                st.rerun()

            else:

                st.error(data["message"])
# =====================================
# SUMMARY
# =====================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "📚 Total Subjects",

        len(subjects)

    )

with col2:

    st.metric(

        "🟢 Safe Subjects",

        len(subjects)

    )

with col3:

    st.metric(

        "⚠ Warning Subjects",

        0

    )