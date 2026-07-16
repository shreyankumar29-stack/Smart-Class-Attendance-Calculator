from models.user import load_user
from flask_login import login_required
from flask_login import LoginManager
from utils.security import bcrypt
from routes.attendance import register_attendance_routes
from routes.analytics import register_analytics_routes
from routes.subjects import register_subject_routes
from routes.auth import register_auth_routes
from flask import Flask, render_template
from db import get_db_connection

app = Flask(__name__)

app.config["SECRET_KEY"] = "24e5840c13e7c782810b4862797a8fc6"

bcrypt.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message_category = "info"


@login_manager.user_loader
def user_loader(user_id):

    return load_user(int(user_id))


register_subject_routes(app)
register_attendance_routes(app)
register_analytics_routes(app)
register_auth_routes(app)

@app.route("/frontend")
def frontend():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.id,
            s.subject_name,
            s.target_percentage,
            COUNT(a.id) AS total_classes,
            COUNT(a.id)
                FILTER (WHERE a.status='Present')
                AS attended_classes
        FROM subjects s
        LEFT JOIN attendance a
            ON s.id = a.subject_id
        GROUP BY
            s.id,
            s.subject_name,
            s.target_percentage
        ORDER BY s.id
    """)

    subjects = cur.fetchall()

    dashboard_data = []

    for row in subjects:

        subject_id = row[0]
        subject_name = row[1]
        target = row[2]
        total = row[3]
        attended = row[4]

        if attended is None:
            attended = 0

        # ==========================
        # ATTENDANCE CALCULATIONS
        # ==========================

        if total == 0:

            percentage = 0
            safe_bunks = 0
            required_classes = 0

        else:

            percentage = (attended / total) * 100

            # Safe Bunks
            safe_bunks = int(
                (attended / (target / 100)) - total
            )

            if safe_bunks < 0:
                safe_bunks = 0

            # Required Classes
            if percentage >= target:

                required_classes = 0

            else:

                required_classes = int(
                    (
                        (target * total)
                        - (100 * attended)
                    )
                    /
                    (
                        100 - target
                    )
                ) + 1

        # ==========================
        # STATUS LOGIC
        # ==========================

        if total == 0:

            status = "NO DATA"

        elif percentage < target:

            status = "WARNING"

        else:

            status = "SAFE"

        # ==========================
        # DEBUG PRINT
        # ==========================

        print(
            "Subject:", subject_name,
            "Target:", target,
            "Total:", total,
            "Present:", attended,
            "Safe:", safe_bunks,
            "Required:", required_classes,
            "Status:", status
        )

        # ==========================
        # DASHBOARD DATA
        # ==========================

        dashboard_data.append({

            "id": subject_id,
            "name": subject_name,
            "target": target,

            "total": total,
            "attended": attended,

            "percentage": round(
                percentage,
                2
            ),

            "safe_bunks": safe_bunks,

            "required_classes":
                required_classes,

            "status": status
        })
    # ==========================
    # SUMMARY DATA
    # ==========================

    total_subjects = len(dashboard_data)

    total_classes = sum(
        subject["total"]
        for subject in dashboard_data
    )

    attended_classes = sum(
        subject["attended"]
        for subject in dashboard_data
    )

    warning_subjects = sum(
        1
        for subject in dashboard_data
        if subject["status"] == "WARNING"
    )

    if total_classes == 0:
        overall_attendance = 0
    else:
        overall_attendance = round(
            (attended_classes / total_classes) * 100,
            2
        )

    # ==========================
    # RECENT ATTENDANCE
    # ==========================

    cur.execute("""
        SELECT
            s.subject_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN subjects s
            ON a.subject_id = s.id
        ORDER BY
            a.attendance_date DESC,
            a.id DESC
        LIMIT 5
    """)

    recent_attendance = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        subjects=dashboard_data,

        total_subjects=total_subjects,
        total_classes=total_classes,
        overall_attendance=overall_attendance,
        warning_subjects=warning_subjects,

        recent_attendance=recent_attendance
    )



# Test Subject Insert
@app.route("/test")
def test():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO subjects
        (subject_name, subject_code, target_percentage)
        VALUES
        ('Data Structures', 'CSR123', 75)
    """)

    conn.commit()

    cur.close()
    conn.close()

    return "Subject Added Successfully"


if __name__ == "__main__":
    app.run(debug=True)