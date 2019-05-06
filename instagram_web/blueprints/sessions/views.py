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
    try:
        # Check if username exists
        user = User.get(User.username == username)
    except:
        # If username is not found, flash an error
        flash("User not found")
        return redirect(url_for("sessions.new"))

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
                flash("Successfully logged in")
                # HAVE A BETTER REDIRECT HERE
                return redirect(url_for("sessions.new"))
            else:
                flash('An error occurred')

    return render_template("sessions/new.html")
