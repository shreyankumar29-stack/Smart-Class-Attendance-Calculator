from flask import jsonify, request

from db import get_db_connection
from models.user import get_user_by_email
from utils.security import verify_password


def register_api_routes(app):

    # =====================================
    # LOGIN API
    # =====================================

    @app.route("/api/login", methods=["POST"])
    def api_login():

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON data received"

            }), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:

            return jsonify({

                "success": False,

                "message": "Email and Password are required"

            }), 400

        user = get_user_by_email(email)

        if user is None:

            return jsonify({

                "success": False,

                "message": "Invalid Email"

            }), 401

        if not verify_password(
            user[4],
            password
        ):

            return jsonify({

                "success": False,

                "message": "Invalid Password"

            }), 401

        return jsonify({

            "success": True,

            "message": "Login Successful",

            "user": {

                "id": user[0],
                "username": user[1],
                "email": user[2]

            }

        }), 200


    # =====================================
    # DASHBOARD API
    # =====================================

    @app.route("/api/dashboard")
    def api_dashboard():

        user_id = request.args.get(
            "user_id",
            type=int
        )

        if not user_id:

            return jsonify({

                "success": False,

                "message": "User ID is required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # =====================================
        # TOTAL SUBJECTS
        # =====================================

        cur.execute(
            """
            SELECT COUNT(*)
            FROM subjects
            WHERE user_id=%s
            """,
            (
                user_id,
            )
        )

        total_subjects = cur.fetchone()[0]

        # =====================================
        # DASHBOARD DATA
        # =====================================

        cur.execute(
            """
            SELECT
                s.target_percentage,
                COUNT(a.id) AS total_classes,
                COUNT(a.id)
                    FILTER (WHERE a.status='Present') AS attended_classes

            FROM subjects s

            LEFT JOIN attendance a
                ON s.id = a.subject_id

            WHERE s.user_id=%s

            GROUP BY
                s.id,
                s.target_percentage
            """,
            (
                user_id,
            )
        )

        rows = cur.fetchall()

        total_classes = 0
        attended_classes = 0
        warning_subjects = 0
        safe_bunks = 0

        for row in rows:

            target = row[0]
            total = row[1]
            attended = row[2]

            if attended is None:
                attended = 0

            total_classes += total
            attended_classes += attended

            if total > 0:

                percentage = (attended / total) * 100

                if percentage < target:

                    warning_subjects += 1

                else:

                    bunks = int(
                        (
                            attended /
                            (target / 100)
                        ) - total
                    )

                    if bunks > 0:

                        safe_bunks += bunks

        if total_classes == 0:

            overall_attendance = 0

        else:

            overall_attendance = round(
                (
                    attended_classes /
                    total_classes
                ) * 100,
                2
            )

        # =====================================
        # RECENT ATTENDANCE
        # =====================================

        cur.execute(
            """
            SELECT
                s.subject_name,
                a.attendance_date,
                a.status

            FROM attendance a

            JOIN subjects s
                ON s.id = a.subject_id

            WHERE s.user_id=%s

            ORDER BY
                a.attendance_date DESC,
                a.id DESC

            LIMIT 5
            """,
            (
                user_id,
            )
        )

        recent_rows = cur.fetchall()

        recent_attendance = []

        for row in recent_rows:

            recent_attendance.append(

                {

                    "subject_name": row[0],

                    "date": str(row[1]),

                    "status": row[2]

                }

            )

        cur.close()
        conn.close()

        return jsonify(

            {

                "total_subjects": total_subjects,

                "overall_attendance": overall_attendance,

                "warning_subjects": warning_subjects,

                "safe_bunks": safe_bunks,

                "recent_attendance": recent_attendance

            }

        )

    # =====================================
    # SUBJECTS API
    # =====================================

    @app.route("/api/subjects")
    def api_subjects():

        user_id = request.args.get(
            "user_id",
            type=int
        )

        if not user_id:

            return jsonify({

                "success": False,

                "message": "User ID is required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                subject_name,
                subject_code,
                target_percentage
            FROM subjects
            WHERE user_id=%s
            ORDER BY subject_name
            """,
            (
                user_id,
            )
        )

        rows = cur.fetchall()

        subjects = []

        for row in rows:

            subjects.append(

                {

                    "id": row[0],

                    "subject_name": row[1],

                    "subject_code": row[2],

                    "target_percentage": row[3]

                }

            )

        cur.close()
        conn.close()

        return jsonify(subjects)

    # =====================================
    # ADD SUBJECT API
    # =====================================

    @app.route("/api/subjects", methods=["POST"])
    def api_add_subject():

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON received"

            }), 400

        user_id = data.get("user_id")
        subject_name = data.get("subject_name")
        subject_code = data.get("subject_code")
        target = data.get("target")

        if not all([

            user_id,
            subject_name,
            subject_code,
            target

        ]):

            return jsonify({

                "success": False,

                "message": "All fields are required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Duplicate subject code check

        cur.execute(

            """
            SELECT id
            FROM subjects
            WHERE user_id=%s
            AND subject_code=%s
            """,

            (

                user_id,
                subject_code

            )

        )

        if cur.fetchone():

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "Subject code already exists"

            }), 409

        cur.execute(

            """
            INSERT INTO subjects
            (
                user_id,
                subject_name,
                subject_code,
                target_percentage
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,

            (

                user_id,
                subject_name,
                subject_code,
                target

            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Subject Added Successfully"

        }), 201

    # =====================================
    # MARK ATTENDANCE API
    # =====================================

    @app.route("/api/attendance", methods=["POST"])
    def api_mark_attendance():

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON received"

            }), 400

        subject_id = data.get("subject_id")
        attendance_date = data.get("attendance_date")
        status = data.get("status")

        if not all([

            subject_id,
            attendance_date,
            status

        ]):

            return jsonify({

                "success": False,

                "message": "All fields are required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Duplicate check

        cur.execute(

            """
            SELECT id
            FROM attendance
            WHERE subject_id=%s
            AND attendance_date=%s
            """,

            (

                subject_id,
                attendance_date

            )

        )

        if cur.fetchone():

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "Attendance already marked"

            }), 409

        cur.execute(

            """
            INSERT INTO attendance
            (
                subject_id,
                attendance_date,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,

            (

                subject_id,
                attendance_date,
                status

            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Attendance Marked Successfully"

        }), 201

    # =====================================
    # DELETE SUBJECT API
    # =====================================

    @app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
    def api_delete_subject(subject_id):

        user_id = request.args.get(
            "user_id",
            type=int
        )

        if not user_id:

            return jsonify({

                "success": False,

                "message": "User ID is required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if subject exists

        cur.execute(

            """
            SELECT id
            FROM subjects
            WHERE id=%s
            AND user_id=%s
            """,

            (
                subject_id,
                user_id
            )

        )

        if cur.fetchone() is None:

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "Subject not found"

            }), 404

        # Delete attendance records first

        cur.execute(

            """
            DELETE FROM attendance
            WHERE subject_id=%s
            """,

            (
                subject_id,
            )

        )

        # Delete subject

        cur.execute(

            """
            DELETE FROM subjects
            WHERE id=%s
            """,

            (
                subject_id,
            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Subject Deleted Successfully"

        }), 200

    # =====================================
    # EDIT SUBJECT API
    # =====================================

    @app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
    def api_edit_subject(subject_id):

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON received"

            }), 400

        subject_name = data.get("subject_name")
        subject_code = data.get("subject_code")
        target = data.get("target")

        if not all([

            subject_name,
            subject_code,
            target

        ]):

            return jsonify({

                "success": False,

                "message": "All fields are required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(

            """
            UPDATE subjects
            SET
                subject_name=%s,
                subject_code=%s,
                target_percentage=%s
            WHERE id=%s
            """,

            (

                subject_name,
                subject_code,
                target,
                subject_id

            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Subject Updated Successfully"

        }), 200