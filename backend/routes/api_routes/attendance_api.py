from flask import jsonify, request

from db import get_db_connection


def register_attendance_api(app):

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

        # =====================================
        # DUPLICATE CHECK
        # =====================================

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

        # =====================================
        # INSERT ATTENDANCE
        # =====================================

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
    # GET ATTENDANCE API
    # =====================================

    @app.route("/api/attendance")
    def api_get_attendance():

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

                a.id,
                s.subject_name,
                a.attendance_date,
                a.status

            FROM attendance a

            JOIN subjects s
                ON a.subject_id = s.id

            WHERE s.user_id=%s

            ORDER BY
                a.attendance_date DESC,
                a.id DESC

            """,

            (
                user_id,
            )

        )

        rows = cur.fetchall()

        attendance = []

        for row in rows:

            attendance.append(

                {

                    "id": row[0],

                    "subject_name": row[1],

                    "attendance_date": str(row[2]),

                    "status": row[3]

                }

            )

        cur.close()
        conn.close()

        return jsonify(attendance)
        # =====================================
    # UPDATE ATTENDANCE API
    # =====================================

    @app.route("/api/attendance/<int:attendance_id>", methods=["PUT"])
    def api_update_attendance(attendance_id):

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON received"

            }), 400

        attendance_date = data.get("attendance_date")
        status = data.get("status")

        if not all([

            attendance_date,
            status

        ]):

            return jsonify({

                "success": False,

                "message": "All fields are required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Check attendance exists

        cur.execute(

            """
            SELECT id
            FROM attendance
            WHERE id=%s
            """,

            (
                attendance_id,
            )

        )

        if cur.fetchone() is None:

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "Attendance record not found"

            }), 404

        # Update attendance

        cur.execute(

            """
            UPDATE attendance
            SET
                attendance_date=%s,
                status=%s
            WHERE id=%s
            """,

            (

                attendance_date,
                status,
                attendance_id

            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Attendance Updated Successfully"

        }), 200
        # =====================================
    # DELETE ATTENDANCE API
    # =====================================

    @app.route("/api/attendance/<int:attendance_id>", methods=["DELETE"])
    def api_delete_attendance(attendance_id):

        conn = get_db_connection()
        cur = conn.cursor()

        # =====================================
        # CHECK ATTENDANCE EXISTS
        # =====================================

        cur.execute(

            """
            SELECT id
            FROM attendance
            WHERE id=%s
            """,

            (
                attendance_id,
            )

        )

        if cur.fetchone() is None:

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "Attendance record not found"

            }), 404

        # =====================================
        # DELETE ATTENDANCE
        # =====================================

        cur.execute(

            """
            DELETE
            FROM attendance
            WHERE id=%s
            """,

            (
                attendance_id,
            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Attendance Deleted Successfully"

        }), 200