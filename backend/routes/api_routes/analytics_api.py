from flask import jsonify, request

from db import get_db_connection


def register_analytics_api(app):

    @app.route("/api/analytics")
    def api_analytics():

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
        # OVERALL STATISTICS
        # =====================================

        cur.execute(

            """
            SELECT

                COUNT(DISTINCT s.id),

                COUNT(a.id),

                COUNT(a.id)
                    FILTER (WHERE a.status='Present'),

                COUNT(a.id)
                    FILTER (WHERE a.status='Absent')

            FROM subjects s

            LEFT JOIN attendance a

                ON s.id = a.subject_id

            WHERE s.user_id=%s
            """,

            (
                user_id,
            )

        )

        row = cur.fetchone()

        total_subjects = row[0] or 0
        total_classes = row[1] or 0
        present_classes = row[2] or 0
        absent_classes = row[3] or 0

        if total_classes == 0:

            overall_attendance = 0

        else:

            overall_attendance = round(

                (present_classes / total_classes) * 100,

                2

            )

        # =====================================
        # SUBJECT WISE ATTENDANCE
        # =====================================

        cur.execute(

            """
            SELECT

                s.subject_name,

                COUNT(a.id) AS total_classes,

                COUNT(a.id)
                    FILTER (WHERE a.status='Present') AS attended_classes,

                s.target_percentage

            FROM subjects s

            LEFT JOIN attendance a

                ON s.id = a.subject_id

            WHERE s.user_id=%s

            GROUP BY

                s.id,
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

        subject_wise = []

        safe_subjects = 0

        warning_subjects = 0

        best_subject = []

        worst_subject = []

        best_percentage = -1

        worst_percentage = 101

        for row in rows:

            subject = row[0]
            total = row[1]
            attended = row[2] or 0
            target = row[3]

            if total == 0:

                percentage = 0

            else:

                percentage = round(

                    (attended / total) * 100,

                    2

                )

            if percentage >= target:

                status = "✅ Safe"

                safe_subjects += 1

            else:

                status = "⚠️ Warning"

                warning_subjects += 1

            subject_wise.append(

                {

                    "subject": subject,

                    "attendance": percentage,

                    "status": status

                }

            )

            # =====================================
            # BEST SUBJECTS
            # =====================================

            if percentage > best_percentage:

                best_percentage = percentage

                best_subjects = [subject]

            elif percentage == best_percentage:

                best_subjects.append(subject)

                # =====================================
                # WORST SUBJECTS
                # =====================================

            if percentage < worst_percentage:

                worst_percentage = percentage

                worst_subjects = [subject]

            elif percentage == worst_percentage:

                worst_subjects.append(subject)

        # =====================================
        # ATTENDANCE TREND
        # =====================================

        cur.execute(

            """
            SELECT

                a.attendance_date,

                COUNT(a.id) AS total_classes,

                COUNT(a.id)
                    FILTER (WHERE a.status='Present') AS present_classes

            FROM attendance a

            JOIN subjects s

                ON a.subject_id = s.id

            WHERE s.user_id=%s

            GROUP BY

                a.attendance_date

            ORDER BY

                a.attendance_date
            """,

            (
                user_id,
            )

        )

        trend_rows = cur.fetchall()

        attendance_trend = []

        for row in trend_rows:

            date = str(row[0])

            total = row[1]

            present = row[2] or 0

            if total == 0:

                percentage = 0

            else:

                percentage = round(

                    (present / total) * 100,

                    2

                )

            attendance_trend.append(

                {

                    "date": date,

                    "attendance": percentage

                }

            )

        cur.close()
        conn.close()

        return jsonify(

            {

                "total_subjects": total_subjects,

                "total_classes": total_classes,

                "present_classes": present_classes,

                "absent_classes": absent_classes,

                "overall_attendance": overall_attendance,

                "safe_subjects": safe_subjects,

                "warning_subjects": warning_subjects,

                "best_subjects": best_subjects,

                "best_percentage": best_percentage,

                "worst_subjects": worst_subjects,

                "worst_percentage": worst_percentage,

                "subject_wise": subject_wise,

                "attendance_trend": attendance_trend

            }

        )