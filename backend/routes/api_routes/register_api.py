from flask import jsonify, request

from db import get_db_connection

from utils.security import bcrypt


def register_register_api(app):

    @app.route("/api/register", methods=["POST"])
    def api_register():

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON received"

            }), 400

        username = data.get("username")

        email = data.get("email")

        password = data.get("password")

        if not all([

            username,
            email,
            password

        ]):

            return jsonify({

                "success": False,

                "message": "All fields are required"

            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # =====================================
        # EMAIL ALREADY EXISTS
        # =====================================

        cur.execute(

            """
            SELECT id
            FROM users
            WHERE email=%s
            """,

            (
                email,
            )

        )

        if cur.fetchone():

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "Email already registered"

            }), 409

        # =====================================
        # HASH PASSWORD
        # =====================================

        hashed_password = bcrypt.generate_password_hash(

            password

        ).decode("utf-8")

        # =====================================
        # INSERT USER
        # =====================================

        cur.execute(

            """
            INSERT INTO users
            (
                username,
                email,
                image_file,
                password
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

                username,

                email,

                "default.jpg",

                hashed_password

            )

        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({

            "success": True,

            "message": "Registration Successful"

        }), 201