import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required
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
    errors = {}

    # Check the length of the username, email and ori_password
    errors.update(length_validation(Username=username, Email=email,
                                    Password=ori_password))

    # Check if passwords match
    if ori_password != request.form.get("confirm"):
        errors.update({"password": "Passwords do not match"})

    # Check for password complexity
    if not pw_complexity(ori_password):
        errors.update(
            {"password": "Include at least one uppercase letter, one lowercase letter, one number and one special character"})

    # Check if email is of a valid format
    if not email_validity(email):
        errors.update({"email": "Enter a valid email"})

    # If errors is an empty array, i.e., there are no errors
    if not errors:
        # Hash user password
        password = generate_password_hash(
            ori_password, method="pbkdf2:sha256", salt_length=8)

        # Create a new instance of a user
        user = User(username=username,
                    email=email, password=password, privacy=request.form.get(
                        "privacy"))
        # Validation
        validator = FormValidator(user)
        # If validation is successful
        if validator.validate():
            user.save()
            flash("Account successfully created")
            return redirect(url_for("users.new"))
        # Else, append the error message
        errors.update(validator.errors)

    return render_template('users/new.html', errors=errors)


@login_required
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
