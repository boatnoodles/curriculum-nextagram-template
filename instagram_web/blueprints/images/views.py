import os
from app import app
from config import S3_BUCKET
from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from instagram_web.blueprints.images.helpers import *
from werkzeug import secure_filename

images_blueprint = Blueprint("images", __name__, template_folder='templates')


@images_blueprint.route("/new", methods=["GET"])
def new():
    breakpoint()
    return render_template("images/new.html")


@images_blueprint.route("/", methods=["POST"])
def create():
    if "user_file" not in request.files:
        flash("No user_file key in request.files")

    file = request.files["user_file"]

    if file.filename == "":
        flash("Please provide a file name")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        return redirect(url_for("images.new"))
    else:
        return "helo"

    return redirect(url_for("images.new"))
