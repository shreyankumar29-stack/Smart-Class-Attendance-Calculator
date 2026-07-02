from db import get_db_connection


def register_analytics_routes(app):

    @app.route("/analytics_test")
    def analytics_test():
        return "Analytics Route Working"


    # ==========================
    # ATTENDANCE PERCENTAGE
    # ==========================
    @app.route("/percentage/<int:subject_id>")
    def percentage(subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                COUNT(*) AS total_classes,
                COUNT(*) FILTER (WHERE status='Present')
                    AS attended_classes
            FROM attendance
            WHERE subject_id=%s
        """, (subject_id,))

        total, attended = cur.fetchone()

        if attended is None:
            attended = 0

        if total == 0:
            percentage = 0
        else:
            percentage = (attended / total) * 100

        cur.close()
        conn.close()

        return f"""
        Subject ID: {subject_id}<br>
        Total Classes: {total}<br>
        Attended Classes: {attended}<br>
        Attendance Percentage: {percentage:.2f}%
        """


    # ==========================
    # SAFE BUNK
    # ==========================
    @app.route("/safe_bunk/<int:subject_id>")
    def safe_bunk(subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                COUNT(*) AS total_classes,
                COUNT(*) FILTER (WHERE status='Present')
                    AS attended_classes
            FROM attendance
            WHERE subject_id=%s
        """, (subject_id,))

        total, attended = cur.fetchone()

        if attended is None:
            attended = 0

        cur.execute("""
            SELECT target_percentage
            FROM subjects
            WHERE id=%s
        """, (subject_id,))

        target = cur.fetchone()[0]

        if total == 0:
            percentage = 0
            bunks = 0
        else:
            percentage = (attended / total) * 100
            bunks = int((attended / (target/100)) - total)

            if bunks < 0:
                bunks = 0

        cur.close()
        conn.close()

        return f"""
        Subject ID: {subject_id}<br>
        Current Attendance: {percentage:.2f}%<br>
        Target Attendance: {target}%<br>
        Safe Bunks Remaining: {bunks}
        """


    # ==========================
    # WARNING
    # ==========================
    @app.route("/warning/<int:subject_id>")
    def warning(subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                COUNT(*) AS total_classes,
                COUNT(*) FILTER (WHERE status='Present')
                    AS attended_classes
            FROM attendance
            WHERE subject_id=%s
        """, (subject_id,))

        total, attended = cur.fetchone()

        if attended is None:
            attended = 0

        if total == 0:
            percentage = 0
        else:
            percentage = (attended / total) * 100

        cur.execute("""
            SELECT target_percentage
            FROM subjects
            WHERE id=%s
        """, (subject_id,))

        target = cur.fetchone()[0]

        cur.close()
        conn.close()

        if percentage < target:
            return f"""
            ⚠ WARNING<br><br>
            Current Attendance: {percentage:.2f}%<br>
            Required Attendance: {target}%<br>
            Your attendance is below the required percentage.
            """

        return f"""
        ✅ Attendance Safe<br><br>
        Current Attendance: {percentage:.2f}%
        """


    # ==========================
    # SINGLE SUBJECT DASHBOARD
    # ==========================
    @app.route("/dashboard/<int:subject_id>")
    def dashboard(subject_id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                subject_name,
                target_percentage
            FROM subjects
            WHERE id=%s
        """, (subject_id,))

        subject = cur.fetchone()

        subject_name = subject[0]
        target = subject[1]

        cur.execute("""
            SELECT
                COUNT(*) AS total_classes,
                COUNT(*) FILTER (WHERE status='Present')
                    AS attended_classes
            FROM attendance
            WHERE subject_id=%s
        """, (subject_id,))

        total, attended = cur.fetchone()

        if attended is None:
            attended = 0

        if total == 0:
            percentage = 0
            safe_bunks = 0
        else:
            percentage = (attended / total) * 100
            safe_bunks = int((attended / (target/100)) - total)

            if safe_bunks < 0:
                safe_bunks = 0

        warning = "SAFE"

        if percentage < target:
            warning = "WARNING"

        cur.close()
        conn.close()

        return f"""
        Subject: {subject_name}<br><br>

        Total Classes: {total}<br>
        Attended Classes: {attended}<br>

        Attendance Percentage:
        {percentage:.2f}%<br><br>

        Safe Bunks:
        {safe_bunks}<br><br>

        Status:
        {warning}
        """


    # ==========================
    # ALL SUBJECTS DASHBOARD
    # ==========================
    @app.route("/dashboard")
    def dashboard_all():

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

        rows = cur.fetchall()

        output = ""

        for row in rows:

            subject_id = row[0]
            subject_name = row[1]
            target = row[2]
            total = row[3]
            attended = row[4]

            if attended is None:
                attended = 0

            if total == 0:
                percentage = 0
                safe_bunks = 0
            else:
                percentage = (attended / total) * 100
                safe_bunks = int(
                    (attended / (target/100)) - total
                )

                if safe_bunks < 0:
                    safe_bunks = 0

            warning = "SAFE"

            if percentage < target:
                warning = "WARNING"

            output += f"""
            <hr>
            <h2>{subject_name}</h2>

            Subject ID: {subject_id}<br>
            Total Classes: {total}<br>
            Attended Classes: {attended}<br>
            Attendance: {percentage:.2f}%<br>
            Safe Bunks: {safe_bunks}<br>
            Status: {warning}<br>
            """

        cur.close()
        conn.close()

        return output
    # ==========================
    # OVERALL ANALYTICS
    # ==========================
    @app.route("/analytics")
    def analytics():

        conn = get_db_connection()
        cur = conn.cursor()

        # Total Subjects
        cur.execute("""
            SELECT COUNT(*)
            FROM subjects
        """)
        total_subjects = cur.fetchone()[0]

        # Total Attendance
        cur.execute("""
            SELECT
                COUNT(*) AS total_classes,
                COUNT(*)
                    FILTER (WHERE status='Present')
            FROM attendance
        """)

        total_classes, attended_classes = cur.fetchone()

        if attended_classes is None:
            attended_classes = 0

        if total_classes == 0:
            overall_attendance = 0
        else:
            overall_attendance = round(
                (attended_classes / total_classes) * 100,
                2
            )

        # Safe and Warning Subjects
        cur.execute("""
            SELECT
                s.target_percentage,
                COUNT(a.id),
                COUNT(a.id)
                    FILTER (WHERE a.status='Present')
            FROM subjects s
            LEFT JOIN attendance a
                ON s.id = a.subject_id
            GROUP BY
                s.id,
                s.target_percentage
        """)

        rows = cur.fetchall()

        safe_subjects = 0
        warning_subjects = 0

        for row in rows:

            target = row[0]
            total = row[1]
            present = row[2]

            if present is None:
                present = 0

            if total == 0:
                percentage = 0
            else:
                percentage = (present / total) * 100

            if percentage >= target:
                safe_subjects += 1
            else:
                warning_subjects += 1

        cur.close()
        conn.close()

        return f"""
        <h1>Overall Analytics</h1>

        Total Subjects:
        {total_subjects}<br><br>

        Total Classes:
        {total_classes}<br><br>

        Attended Classes:
        {attended_classes}<br><br>

        Overall Attendance:
        {overall_attendance}%<br><br>

        Safe Subjects:
        {safe_subjects}<br><br>

        Warning Subjects:
        {warning_subjects}
        """
    # ==========================
    # RECENT ATTENDANCE
    # ==========================
    @app.route("/recent_attendance")
    def recent_attendance():

        conn = get_db_connection()
        cur = conn.cursor()

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
            LIMIT 10
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        if not rows:
            return "No attendance records found"

        output = "<h1>Recent Attendance</h1><br>"

        for row in rows:

            subject = row[0]
            date = row[1]
            status = row[2]

            output += f"""
            {date} |
            {subject} |
            {status}
            <br><br>
            """

        return output
    # ==========================
    # HEALTH CHECK
    # ==========================
    @app.route("/health")
    def health():

        try:

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT 1")

            cur.close()
            conn.close()

            return {
                "status": "running",
                "database": "connected",
                "backend": "healthy"
            }

        except:

            return {
                "status": "error",
                "database": "disconnected"
            }
