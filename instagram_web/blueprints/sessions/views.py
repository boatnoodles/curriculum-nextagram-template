from flask import Blueprint, Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user
from models.user import User
from werkzeug.security import check_password_hash
from instagram_web.util.helpers.oauth import google_oauth, facebook_oauth


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
        flash("User not found", "danger")
        # return render_template("sessions/new.html")
        return redirect(url_for("sessions.new"))

    # Get passwords
    form_pw = request.form.get("password")
    user = User.get(User.username == username)
    db_pw = user.password

    # Compare user hash and db hash
    if not check_password_hash(db_pw, form_pw):
        # If password is incorrect
        flash("Incorrect password", "danger")
        return redirect(url_for("sessions.new"))

    # Allow user to log in
    if not login_user(user):
        flash('An error occurred')

    # Redirect to profile page/home page or what was the user at previously
    flash("Successfully logged in", "success")
    return redirect(url_for('home'))


#
@sessions_blueprint.route("/delete", methods=["POST"])
def delete():
    logout_user()
    flash("Successfully logged out", "success")
    return redirect(url_for("sessions.new"))


@sessions_blueprint.route("/google_login/authorize", methods=["GET"])
def google_authorize():
    token = google_oauth.google.authorize_access_token()
    if token:
        email = google_oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        user = User.get_or_none(User.email == email)
        if not user:
            flash('No user registered with this email')
            return redirect(url_for('sessions.new'))
    flash(f'Hello {user.username}', "info")
    login_user(user)
    return redirect(url_for("home", username=user.username))


@sessions_blueprint.route("/google_login", methods=["GET"])
def google_login():
    redirect_uri = url_for('sessions.google_authorize', _external=True)
    return google_oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/facebook_login/authorize", methods=["GET"])
def facebook_authorize():
    token = facebook_oauth.facebook.authorize_access_token()
    if token:
        email = facebook_oauth.facebook.get('https://www.').json()['email']
        user = User.get_or_none(User.email == email)
        if not user:
            flash('No user registered with this email')
            return redirect(url_for('sessions.new'))
    flash(f'Hello {user.username}')
    return redirect(url_for("sessions.facebook_login"))


@sessions_blueprint.route("/facebook_login", methods=["GET"])
def facebook_login():
    redirect_uri = url_for('sessions.facebook_authorize', _external=True)
    return facebook_oauth.facebook.authorize_redirect(redirect_uri)


# https: // www.facebook.com/v3.3/dialog/oauth?
# client_id = {app-id}
# &redirect_uri = {redirect-uri}
# &state = {state-param}
