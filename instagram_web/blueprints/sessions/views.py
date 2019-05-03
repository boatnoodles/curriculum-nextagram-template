from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from flask.ext.session import Session
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route('/new', methods=['GET'])
# Log in page
def new():
    render_template("new.html")


@sessions_blueprint.route("/", methods=["POST"])
# Handles user log in by creating a new session
def create():
    # Gets the username
    # Gets the password (check hash)
    # Compare user hash and db hash
    # If valid, create a new session
