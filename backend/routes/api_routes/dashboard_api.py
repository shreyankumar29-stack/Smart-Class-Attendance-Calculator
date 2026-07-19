from flask import jsonify, request

from db import get_db_connection


def register_dashboard_api(app):

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
    # SUBJECT OVERVIEW API
    # =====================================

    @app.route("/api/dashboard/subjects")
    def api_dashboard_subjects():

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

                s.subject_name,

                s.target_percentage,

                COUNT(a.id) AS total_classes,

                COUNT(a.id)
                FILTER
                (
                    WHERE a.status='Present'
                ) AS attended_classes

            FROM subjects s

            LEFT JOIN attendance a
            ON s.id=a.subject_id

            WHERE s.user_id=%s

            GROUP BY

                s.subject_name,
                s.target_percentage

            ORDER BY
                s.subject_name

            """,

            (
                user_id,
            )

        )

        rows = cur.fetchall()

        subjects = []

        for row in rows:

            subject = row[0]
            target = row[1]
            total = row[2]
            attended = row[3]

            if attended is None:

                attended = 0

            if total == 0:

                percentage = 0
                safe_bunks = 0

            else:

                percentage = round(

                    (
                        attended /
                        total
                    ) * 100,

                    2

                )

                safe_bunks = int(

                    (
                        attended /
                        (target / 100)
                    ) - total

                )

                if safe_bunks < 0:

                    safe_bunks = 0

            if percentage >= target:

                status = "✅ Safe"

            else:

                status = "⚠ Warning"

            subjects.append(

                {

                    "Subject": subject,

                    "Attendance %": percentage,

                    "Safe Bunks": safe_bunks,

                    "Status": status

                }

            )

        cur.close()
        conn.close()

        return jsonify(subjects)