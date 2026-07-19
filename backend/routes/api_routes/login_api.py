from flask import jsonify, request

from models.user import get_user_by_email
from utils.security import verify_password


def register_login_api(app):

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