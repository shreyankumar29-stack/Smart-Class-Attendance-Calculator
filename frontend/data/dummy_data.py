# =====================================
# DUMMY DATA
# =====================================

DUMMY_SUBJECTS = [

    {

        "subject_name": "Computer Architecture",

        "subject_code": "CSR126",

        "target_percentage": 75

    },

    {

        "subject_name": "Database Design",

        "subject_code": "CSR122",

        "target_percentage": 75

    }

]


DUMMY_ATTENDANCE = [

    {

        "subject_name": "Computer Architecture",

        "attendance_date": "2026-07-20",

        "status": "Present"

    },

    {

        "subject_name": "Database Design",

        "attendance_date": "2026-07-21",

        "status": "Absent"

    }

]


DUMMY_DASHBOARD = {

    "total_subjects": 2,

    "overall_attendance": 75,

    "warning_subjects": 1,

    "safe_bunks": 2

}


"""
Dummy data for frontend testing.

Currently unused because the application
uses live data from Flask APIs.
"""