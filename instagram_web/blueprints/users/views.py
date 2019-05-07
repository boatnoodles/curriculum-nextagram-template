import os
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from instagram_web.blueprints.users.helpers import *
from models.user import *
from peewee_validates import ModelValidator, StringField, validate_length
from werkzeug.security import generate_password_hash


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
    username = request.form.get("username")
    email = request.form.get("email")
    ori_password = request.form.get("password")

    errors = form_validation(
        username, email, ori_password, request.form.get("confirm"))

    # If errors is an empty array, i.e., there are no errors
    if not errors:
        # Hash user password
        password = generate_password_hash(
            ori_password, method="pbkdf2:sha256", salt_length=8)

        # Create a new instance of a user
        user = User(username=username,
                    email=email, password=password, privacy=request.form.get(
                        "privacy"))
        # Validation using peewee-validates's ModelValidator
        validator = FormValidator(user)
        # If validation is successful
        if validator.validate():
            user.save()
            flash("Account successfully created")
            return redirect(url_for("users.new"))
        # Else, append the error message
        errors.update(validator.errors)

    return render_template('users/new.html', errors=errors)


# Display user profile page
@users_blueprint.route('/<username>', methods=["GET"])
@login_required
# Personal profile page
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


# Display page to edit user information
@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if current_user != User.get_by_id(id):
        return abort(403)
    username = current_user.username
    email = current_user.email
    user_id = current_user.id
    return render_template("users/edit.html", username=username, email=email, user_id=user_id)

# Edit user information
@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    # Get the necessary information from the form
    username = request.form.get("username")
    email = request.form.get("email")
    new_password = request.form.get("password")

    # Compare with old info?
    # current_user.username
    # If no changes have been made, let the user know
    errors = form_validation(
        username, email, new_password, request.form.get("confirm"))

    # If errors is an empty array, i.e., there are no errors
    if not errors:
        # Hash user password
        password = generate_password_hash(
            new_password, method="pbkdf2:sha256", salt_length=8)

        # Update user
        user = User.update({User.username: username, User.email: email,
                            User.password: password, User.privacy: request.form.get("privacy")}).where(User.id == current_user.id)
        # Validation using peewee-validates's ModelValidator
        validator = FormValidator(user)
        # If validation is successful
        if validator.validate():
            user.execute()
            flash("Account successfully updated")
            return redirect(url_for("users.edit"))
        # Else, append the error message
        errors.update(validator.errors)

    return render_template('users/edit.html', errors=errors)
