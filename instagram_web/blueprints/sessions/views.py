from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from flask_login import login_user
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    # Log in page
    return render_template("sessions/new.html")


@sessions_blueprint.route("/", methods=["POST"])
# Handle user log in by creating a new session
def create():
    # Get the user input
    username = request.form.get("username")
    # Check if username exists, if not, flash error
    user = User.get(User.username == username)

    # If username is not found
    if not user:
        # Throw an error
        flash("User not found")

    # Get passwords
    else:
        form_pw = request.form.get("password")
        user = User.get(User.username == username)
        db_pw = user.password
        # Compare user hash and db hash
        # If valid, log user in
        if check_password_hash(db_pw, form_pw):
            # Allow user to log in
            if login_user(user):
                # Redirect to profile page/home page
                # HAVE A BETTER REDIRECT HERE
                return redirect(url_for("home"))
            else:
                flash('An error occurred')

    return render_template("sessions/new.html")
