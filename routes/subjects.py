from flask import request, redirect
from db import get_db_connection


def register_subject_routes(app):

    # =====================================
    # ADD SUBJECT
    # =====================================
    @app.route("/add_subject")
    def add_subject():

        subject_name = request.args.get("subject_name")
        subject_code = request.args.get("subject_code")
        target = request.args.get("target")

        # Empty validation
        if not subject_name or not subject_code or not target:
            return "Error: All fields are required"

        # Target validation
        try:
            target = int(target)

            if target < 0 or target > 100:
                return "Error: Target percentage must be between 0 and 100"

        except:
            return "Error: Invalid target percentage"

        conn = get_db_connection()
        cur = conn.cursor()

        # Duplicate subject code
        cur.execute("""
            SELECT *
            FROM subjects
            WHERE subject_code=%s
        """, (subject_code,))

        existing = cur.fetchone()

        if existing:
            cur.close()
            conn.close()

            return "Error: Subject code already exists"

        # Insert
        cur.execute("""
            INSERT INTO subjects
            (
                subject_name,
                subject_code,
                target_percentage
            )
            VALUES (%s,%s,%s)
        """,
        (
            subject_name,
            subject_code,
            target
        ))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/frontend")


    # =====================================
    # DELETE SUBJECT
    # =====================================
    @app.route("/delete_subject/<int:id>")
    def delete_subject(id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM subjects
            WHERE id=%s
        """, (id,))

        subject = cur.fetchone()

        if not subject:

            cur.close()
            conn.close()

            return "Error: Subject not found"

        # ON DELETE CASCADE
        cur.execute("""
            DELETE FROM subjects
            WHERE id=%s
        """, (id,))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/frontend")


    # =====================================
    # EDIT SUBJECT
    # =====================================
    @app.route("/edit_subject/<int:id>")
    def edit_subject(id):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                subject_name,
                subject_code,
                target_percentage
            FROM subjects
            WHERE id=%s
        """, (id,))

        subject = cur.fetchone()

        cur.close()
        conn.close()

        if not subject:
            return "Error: Subject not found"

        return f"""
        <h2>Edit Subject</h2>

        <form action="/update_subject/{id}">

            Subject Name:
            <input
                type="text"
                name="subject_name"
                value="{subject[1]}">

            <br><br>

            Subject Code:
            <input
                type="text"
                name="subject_code"
                value="{subject[2]}">

            <br><br>

            Target Percentage:
            <input
                type="number"
                name="target"
                value="{subject[3]}">

            <br><br>

            <button type="submit">
                Update Subject
            </button>

        </form>
        """


    # =====================================
    # UPDATE SUBJECT
    # =====================================
    @app.route("/update_subject/<int:id>")
    def update_subject(id):

        subject_name = request.args.get("subject_name")
        subject_code = request.args.get("subject_code")
        target = request.args.get("target")

        # Empty validation
        if not subject_name or not subject_code or not target:
            return "Error: All fields are required"

        # Target validation
        try:

            target = int(target)

            if target < 0 or target > 100:
                return "Error: Target percentage must be between 0 and 100"

        except:
            return "Error: Invalid target percentage"

        conn = get_db_connection()
        cur = conn.cursor()

        # Subject exists?
        cur.execute("""
            SELECT *
            FROM subjects
            WHERE id=%s
        """, (id,))

        subject = cur.fetchone()

        if not subject:

            cur.close()
            conn.close()

            return "Error: Subject not found"

        # Duplicate code check
        cur.execute("""
            SELECT *
            FROM subjects
            WHERE subject_code=%s
            AND id<>%s
        """, (subject_code, id))

        duplicate = cur.fetchone()

        if duplicate:

            cur.close()
            conn.close()

            return "Error: Subject code already exists"

        # Update
        cur.execute("""
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
            id
        ))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/frontend")