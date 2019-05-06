from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from flask.ext.session import Session
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route('/new', methods=['GET'])
# Log in page
def new():
    render_template("new.html")


@sessions_blueprint.route("/", methods=["POST"])
# Handle user log in by creating a new session
def create():
    # Get the user input
    username = request.form.get("username")
    # Check if username exists, if not, flash error
    u = User.select().where(User.username == username)

    # If username is not found
    if not u:
        # Throw an error
        flash("User not found")
    else:
        # Get passwords
        form_pw = request.form.get("password")
        db_pw = User.select().where(User.username == username)
        # Compare user hash and db hash
        # If valid, create a new session
        if check_password_hash(db_pw, form_pw):
            # Allow user to log in

            return redirect(url_for("users.new"))

    return render_template("sessions/new.html")
