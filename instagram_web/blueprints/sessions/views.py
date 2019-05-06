from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    # Log in page
    return render_template("sessions/new.html")

# Log user in
@sessions_blueprint.route("/", methods=["POST"])
def create():
    # Handle user log in by creating a new session
    # Get the user input
    username = request.form.get("username")

    # Check if username exists
    user = User.get_or_none(User.username == username)

    if not user:
        # If username is not found, flash an error
        flash("User not found")
        return render_template("sessions/new.html")
        # return redirect(url_for("sessions.new"))

    # Get passwords
    form_pw = request.form.get("password")
    user = User.get(User.username == username)
    db_pw = user.password

    # Compare user hash and db hash
    if not check_password_hash(db_pw, form_pw):
        # If password is incorrect
        flash("Incorrect password")
        return redirect(url_for("sessions.new"))

    # Allow user to log in
    if not login_user(user):
        flash('An error occurred')

    # Redirect to profile page/home page
    flash("Successfully logged in")

    """HAVE A BETTER REDIRECT HERE"""
    return redirect(url_for("sessions.new"))


#
@sessions_blueprint.route("/delete", methods=["POST"])
def delete():
    logout_user()
    flash("Successfully logged out")
    return redirect(url_for("sessions.new"))
