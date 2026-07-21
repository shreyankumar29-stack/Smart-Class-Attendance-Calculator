from flask import (
    jsonify,
    request,
    current_app
)
from utils.security import (
    verify_password,
    hash_password
)
import os
import uuid

from werkzeug.utils import secure_filename

from db import get_db_connection


# =====================================
# ALLOWED IMAGE TYPES
# =====================================

ALLOWED_EXTENSIONS = {

    "png",

    "jpg",

    "jpeg"

}


def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(".", 1)[1].lower()

        in ALLOWED_EXTENSIONS

    )


# =====================================
# REGISTER PROFILE API
# =====================================

def register_profile_api(app):
    # =====================================
    # GET PROFILE
    # =====================================

    @app.route("/api/profile", methods=["GET"])
    def api_profile():

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
                username,
                email,
                image_file

            FROM users

            WHERE id=%s
            """,

            (
                user_id,
            )

        )

        row = cur.fetchone()

        if row is None:

            cur.close()
            conn.close()

            return jsonify({

                "success": False,

                "message": "User not found"

            }), 404

        profile = {

            "id": row[0],

            "username": row[1],

            "email": row[2],

            "image_file": row[3]

        }

        cur.close()
        conn.close()

        return jsonify(profile)
        # =====================================
    # UPLOAD PROFILE PICTURE
    # =====================================

    @app.route("/api/profile/upload", methods=["POST"])
    def api_upload_profile_picture():

        user_id = request.form.get(

            "user_id",

            type=int

        )

        if not user_id:

            return jsonify({

                "success": False,

                "message": "User ID is required"

            }), 400

        if "image" not in request.files:

            return jsonify({

                "success": False,

                "message": "No image uploaded"

            }), 400

        image = request.files["image"]

        if image.filename == "":

            return jsonify({

                "success": False,

                "message": "No image selected"

            }), 400

        if not allowed_file(image.filename):

            return jsonify({

                "success": False,

                "message": "Only PNG, JPG and JPEG files are allowed"

            }), 400

        extension = image.filename.rsplit(

            ".",

            1

        )[1].lower()

        unique_filename = (

            str(uuid.uuid4())

            + "."

            + extension

        )

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(

            upload_folder,

            exist_ok=True

        )

        image_path = os.path.join(

            upload_folder,

            unique_filename

        )

        image.save(image_path)

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute(

            """
            SELECT image_file

            FROM users

            WHERE id=%s
            """,

            (
                user_id,
            )

        )

        row = cur.fetchone()

        old_image = row[0] if row else "default.jpg"

        cur.execute(

            """
            UPDATE users

            SET image_file=%s

            WHERE id=%s
            """,

            (
                unique_filename,
                user_id
            )

        )

        conn.commit()

        if (

            old_image

            and

            old_image != "default.jpg"

        ):

            old_image_path = os.path.join(

                upload_folder,

                old_image

            )

            if os.path.exists(old_image_path):

                os.remove(old_image_path)

        cur.close()

        conn.close()

        return jsonify({

            "success": True,

            "message": "Profile picture updated successfully.",

            "image_file": unique_filename

        }), 200
        # =====================================
    # REMOVE PROFILE PICTURE
    # =====================================

    @app.route("/api/profile/remove", methods=["POST"])
    def api_remove_profile_picture():

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "Invalid request"

            }), 400

        user_id = data.get("user_id")

        if not user_id:

            return jsonify({

                "success": False,

                "message": "User ID is required"

            }), 400

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute(

            """
            SELECT image_file

            FROM users

            WHERE id=%s
            """,

            (
                user_id,
            )

        )

        row = cur.fetchone()

        if row is None:

            cur.close()

            conn.close()

            return jsonify({

                "success": False,

                "message": "User not found"

            }), 404

        old_image = row[0]

        cur.execute(

            """
            UPDATE users

            SET image_file='default.jpg'

            WHERE id=%s
            """,

            (
                user_id,
            )

        )

        conn.commit()

        cur.close()

        conn.close()

        if old_image and old_image != "default.jpg":

            old_path = os.path.join(

                current_app.config["UPLOAD_FOLDER"],

                old_image

            )

            if os.path.exists(old_path):

                os.remove(old_path)

        return jsonify({

            "success": True,

            "message": "Profile picture removed successfully."

        }), 200
        # =====================================
    # CHANGE PASSWORD
    # =====================================

    @app.route("/api/profile/change-password", methods=["POST"])
    def api_change_password():

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "Invalid request"

            }), 400

        user_id = data.get("user_id")

        current_password = data.get("current_password")

        new_password = data.get("new_password")

        confirm_password = data.get("confirm_password")

        if not all([

            user_id,

            current_password,

            new_password,

            confirm_password

        ]):

            return jsonify({

                "success": False,

                "message": "All fields are required"

            }), 400

        if new_password != confirm_password:

            return jsonify({

                "success": False,

                "message": "New passwords do not match"

            }), 400

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute(

            """
            SELECT password

            FROM users

            WHERE id=%s
            """,

            (
                user_id,
            )

        )

        row = cur.fetchone()

        if row is None:

            cur.close()

            conn.close()

            return jsonify({

                "success": False,

                "message": "User not found"

            }), 404

        if not verify_password(

            row[0],

            current_password

        ):

            cur.close()

            conn.close()

            return jsonify({

                "success": False,

                "message": "Current password is incorrect"

            }), 401

        hashed_password = hash_password(

            new_password

        )

        cur.execute(

            """
            UPDATE users

            SET password=%s

            WHERE id=%s
            """,

            (
                hashed_password,

                user_id
            )

        )

        conn.commit()

        cur.close()

        conn.close()

        return jsonify({

            "success": True,

            "message": "Password changed successfully."

        }), 200