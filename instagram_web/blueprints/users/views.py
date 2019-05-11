import os
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user
from peewee_validates import ModelValidator, StringField, validate_length
from werkzeug.security import generate_password_hash
# USER-DEFINED MODULES
from instagram_web.util.helpers.users import *
from instagram_web.util.helpers.uploads import *
from models.user import *


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
# Sign up page
def new():
    errors = {}
    return render_template('users/new.html', errors={})


@users_blueprint.route('/', methods=['POST'])
# Handles user sign up
def create():
    keys = ["username", "email", "password", "confirm"]
    to_validate = {}
    for key in keys:
        to_validate[key] = request.form.get(key)

    errors = form_validation(to_validate)

    # If errors is an empty array, i.e., there are no errors
    if not errors:
        # Hash user password
        password = generate_password_hash(
            to_validate["password"], method="pbkdf2:sha256", salt_length=8)

        # Create a new instance of a user
        user = User(username=to_validate["username"],
                    email=to_validate["email"],
                    password=password, privacy=request.form.get("privacy"))

        # Validation using peewee-validates's ModelValidator
        validator = FormValidator(user)
        # If validation is successful
        if validator.validate():
            if user.save():
                flash("Account successfully created")
                login_user(user)
                return redirect(url_for("home"))
        # Else, append the error message
        errors.update(validator.errors)

    return render_template('users/new.html', errors=errors)


# Display user profile page
@users_blueprint.route('/<username>', methods=["GET"])
@login_required
# Personal profile page
def show(username):
    user = User.get(User.username == username)
    posts = user.posts
    return render_template("users/show.html", user=user, posts=posts)
    # for post in posts post.path, post.caption


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


# Display page to edit user information
@users_blueprint.route('/<username>/edit', methods=['GET'])
@login_required
def edit(username):
    try:
        user = User.get(User.username == username)
        if current_user != user:
            return abort(403)
    except:
        return "USERNAME DOES NOT EXIST"

    user = User.get_by_id(current_user.id)
    img = user.profile_picture_url
    return render_template("users/edit.html", user=user, img=img)

# Edit user information
@users_blueprint.route('/<username>/update', methods=['POST'])
@login_required
def update(username):
    # Get the necessary information from the form and compare it with current_info
    keys = ["username", "email"]
    to_be_changed = {}
    for key in keys:
        field = request.form.get(key)
        # If form field is not blank
        if field != "":
            # If the field is confirm or the field is not equal to what is stored in sessions with the same key
            if field != getattr(current_user, key):
                to_be_changed[key] = field
    # Attempts to upload file
    if request.files:
        url_path = handle_upload("user_file", route="images")
        to_be_changed["profile_picture"] = url_path

    # If no changes have been made, let the user know
    if not to_be_changed and not url_path:
        flash("No changes were made", "info")
        return redirect(url_for("users.edit", username=username))

    # Validate user's input
    errors = form_validation(to_be_changed)
    # If there are errors
    if not errors:
        # # Hash user password only if password has been filled in
        # try:
        #     password = to_be_changed["password"]
        # except KeyError:
        #     password = None
        # if password:
        #     to_be_changed["password"] = generate_password_hash(
        #         to_be_changed["password"], method="pbkdf2:sha256", salt_length=8)
        # privacy = request.form.get("privacy"),
        # Obtain privacy option
        user = User.update(update_queries(to_be_changed, privacy=request.form.get("privacy"))
                           ).where(User.id == current_user.id)
        # If unable to perform the update query
        if not user.execute():
            errors.update(
                "An error occurred, please try again later", "warning")
            return redirect(url_for("users.edit", id=id), errors=errors)

        # Notify user that the change has been successfully made
        flash("Account successfully updated", "success")
        return redirect(url_for("users.edit", username=request.form.get("username")))

    return redirect(url_for("users.edit", username=request.form.get("username")))
