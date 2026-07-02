from flask import request, redirect, render_template
from db import get_db_connection


def register_attendance_routes(app):

    # =====================================
    # ADD ATTENDANCE
    # =====================================
    @app.route("/add_attendance")
    def add_attendance():

        subject_id = request.args.get("subject_id")
        status = request.args.get("status")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO attendance
            (subject_id, attendance_date, status)
            VALUES (%s, CURRENT_DATE, %s)
        """, (subject_id, status))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/frontend")


    # =====================================
    # VIEW ATTENDANCE RECORDS
    # =====================================
    @app.route("/attendance/<int:subject_id>")
    def attendance(subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM attendance
            WHERE subject_id=%s
            ORDER BY id
        """, (subject_id,))

        data = cur.fetchall()

        cur.close()
        conn.close()

        return str(data)


    # =====================================
    # EDIT ATTENDANCE
    # =====================================
    @app.route("/edit_attendance/<int:id>/<int:subject_id>")
    def edit_attendance(id, subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                status
            FROM attendance
            WHERE id=%s
        """, (id,))

        attendance = cur.fetchone()

        if attendance is None:

            cur.close()
            conn.close()

            return "Attendance Record Not Found"

        current_status = attendance[0]

        # Toggle Present/Absent
        if current_status == "Present":
            new_status = "Absent"
        else:
            new_status = "Present"

        cur.execute("""
            UPDATE attendance
            SET status=%s
            WHERE id=%s
        """, (
            new_status,
            id
        ))

        conn.commit()

        cur.close()
        conn.close()

        return redirect(
            f"/attendance_history/{subject_id}"
        )


    # =====================================
    # DELETE ATTENDANCE
    # =====================================
    @app.route("/delete_attendance/<int:id>/<int:subject_id>")
    def delete_attendance(id, subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM attendance
            WHERE id=%s
        """, (id,))

        conn.commit()

        cur.close()
        conn.close()

        return redirect(
            f"/attendance_history/{subject_id}"
        )


    # =====================================
    # TEST ROUTE
    # =====================================
    @app.route("/history_test")
    def history_test():

        return "History Route Working"


    # =====================================
    # ATTENDANCE HISTORY
    # =====================================
    @app.route("/attendance_history/<int:subject_id>")
    def attendance_history(subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        # Subject Details
        cur.execute("""
            SELECT
                subject_name,
                target_percentage
            FROM subjects
            WHERE id=%s
        """, (subject_id,))

        subject = cur.fetchone()

        if subject is None:

            cur.close()
            conn.close()

            return "Subject Not Found"

        subject_name = subject[0]
        target = subject[1]

        # Attendance History
        cur.execute("""
            SELECT
                id,
                attendance_date,
                status
            FROM attendance
            WHERE subject_id=%s
            ORDER BY
                attendance_date DESC,
                id DESC
        """, (subject_id,))

        history = cur.fetchall()

        # Statistics
        total_classes = len(history)

        present_classes = sum(
            1
            for row in history
            if row[2] == "Present"
        )

        absent_classes = total_classes - present_classes

        if total_classes == 0:
            percentage = 0
        else:
            percentage = round(
                (present_classes / total_classes) * 100,
                2
            )
        # ==========================
        # PROGRESS ANALYTICS
        # ==========================

        if percentage >= target:

            trend = "Excellent"

        elif percentage >= target - 10:

           trend = "Improving"

        elif percentage >= target - 20:

            trend = "Satisfactory"

        elif percentage >= target - 30:

            trend = "Average"

        else:

            trend = "Critical"
        cur.close()
        conn.close()

        return render_template(
            "history.html",

            subject_id=subject_id,
            subject_name=subject_name,
            target=target,

            history=history,

            total_classes=total_classes,
            present_classes=present_classes,
            absent_classes=absent_classes,
            percentage=percentage,trend=trend
        )
