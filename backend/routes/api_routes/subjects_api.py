from flask import jsonify, request

from db import get_db_connection


def register_subjects_api(app):

    # =====================================
    # GET SUBJECTS API
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

                s.id,

                s.subject_name,

                s.subject_code,

                s.target_percentage,

                COUNT(a.id) AS total_classes,

                COUNT(a.id)
                FILTER
                (
                    WHERE a.status='Present'
                ) AS attended_classes

            FROM subjects s

            LEFT JOIN attendance a
                ON s.id = a.subject_id

            WHERE s.user_id=%s

            GROUP BY

                s.id,
                s.subject_name,
                s.subject_code,
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

            total = row[4]
            attended = row[5]

            if attended is None:
                attended = 0

            if total == 0:

                percentage = 0
                status = "⚠️ Warning"

            else:

                percentage = round(

                    (
                        attended /
                        total
                    ) * 100,

                    2

                )

                if percentage >= row[3]:

                    status = "✅ Safe"

                else:

                    status = "⚠️ Warning"

            subjects.append(

                {

                    "id": row[0],

                    "subject_name": row[1],

                    "subject_code": row[2],

                    "target_percentage": row[3],

                    "attendance_percentage": percentage,

                    "status": status

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
    # UPDATE SUBJECT API
    # =====================================

    @app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
    def api_update_subject(subject_id):

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

        # Check subject exists

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

        # Delete attendance first

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