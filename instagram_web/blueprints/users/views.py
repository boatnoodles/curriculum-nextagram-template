from flask import Blueprint, redirect, render_template, request, url_for
from helpers import *
# from instagram_web.forms.forms import *
from models.user import *
from werkzeug.security import check_password_hash, generate_password_hash
from peewee_validates import ModelValidator, StringField, validate_length


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("username")
    email = request.form.get("email")
    ori_password = request.form.get("password")
    errors = []

    # Check the length of the username, email and ori_password
    length_errors = length_validation(Username=username, Email=email,
                                      Password=ori_password)
    for key, value in length_errors.items():
        errors.append(value)

    # Check if passwords match
    if ori_password != request.form.get("confirm"):
        errors.append("Passwords do not match")

    # If errors is an empty array, i.e., there are no errors
    if not errors:
        # Hash user password
        password = generate_password_hash(
            ori_password, method="pbkdf2:sha256", salt_length=8)

        # Create a new instance of a user
        user = User(username=username,
                    email=email, password=password)
        # Validation
        validator = FormValidator(user)
        # If validation is successful
        if validator.validate():
            user.save()
            return redirect(url_for("users.new"))
        # Else, append the error message
        for key, value in validator.errors.items():
            errors.append(value)

    return render_template('users/new.html', errors=errors)


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
