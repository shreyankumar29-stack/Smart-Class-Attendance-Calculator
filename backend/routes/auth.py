import os
import secrets

from PIL import Image
from flask import current_app
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from forms.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm
)

from models.user import (
    User,
    create_user,
    get_user_by_email,
    get_user_by_username,
    update_user
)

from utils.security import (
    hash_password,
    verify_password
)


def save_picture(form_picture):

    random_hex = secrets.token_hex(8)

    _, file_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + file_ext

    picture_path = os.path.join(
        current_app.root_path,
        "static",
        "profile_pics",
        picture_fn
    )

    output_size = (125, 125)

    img = Image.open(form_picture)

    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_fn


def register_auth_routes(app):


    # =====================================
    # HOME
    # =====================================

    @app.route("/")
    @app.route("/home")
    def home():

        return render_template(
            "home.html",
            title="Home"
        )

    # =====================================
    # REGISTER
    # =====================================

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if current_user.is_authenticated:

            return redirect(
                url_for("frontend")
            )

        form = RegistrationForm()

        if form.validate_on_submit():

            if get_user_by_username(form.username.data):

                flash(
                    "Username already exists.",
                    "danger"
                )

                return render_template(
                    "register.html",
                    title="Register",
                    form=form
                )

            if get_user_by_email(form.email.data):

                flash(
                    "Email already exists.",
                    "danger"
                )

                return render_template(
                    "register.html",
                    title="Register",
                    form=form
                )

            hashed_password = hash_password(
                form.password.data
            )

            create_user(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )

            flash(
                "Your account has been created successfully! Please login.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        return render_template(
            "register.html",
            title="Register",
            form=form
        )

    # =====================================
    # LOGIN
    # =====================================

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if current_user.is_authenticated:

            return redirect(
                url_for("frontend")
            )

        form = LoginForm()

        if form.validate_on_submit():

            user = get_user_by_email(
                form.email.data
            )

            if user and verify_password(
                user[4],
                form.password.data
            ):

                login_user(

                    User(
                        id=user[0],
                        username=user[1],
                        email=user[2],
                        image_file=user[3],
                        password=user[4]
                    ),

                    remember=form.remember.data

                )

                flash(
                    "Login Successful.",
                    "success"
                )

                return redirect(
                    url_for("frontend")
                )

            flash(
                "Login Unsuccessful. Please check email and password.",
                "danger"
            )

        return render_template(
            "login.html",
            title="Login",
            form=form
        )

    # =====================================
    # LOGOUT
    # =====================================

    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        flash(
            "You have been logged out.",
            "info"
        )

        return redirect(
            url_for("home")
        )

    # =====================================
    # ACCOUNT
    # =====================================

    @app.route("/account", methods=["GET", "POST"])
    @login_required
    def account():

        form = UpdateAccountForm()

        if form.validate_on_submit():

            image_file = current_user.image_file

            if form.picture.data:

                image_file = save_picture(
                    form.picture.data
                )

            update_user(

                user_id=current_user.id,

                username=form.username.data,

                email=form.email.data,

                image_file=image_file

            )

            flash(
                "Your account has been updated!",
                "success"
            )

            return redirect(
                url_for("account")
            )

        elif request.method == "GET":

            form.username.data = current_user.username

            form.email.data = current_user.email

        image_file = url_for(
            "static",
            filename="profile_pics/" + current_user.image_file
        )

        return render_template(
            "account.html",
            title="Account",
            image_file=image_file,
            form=form
        )