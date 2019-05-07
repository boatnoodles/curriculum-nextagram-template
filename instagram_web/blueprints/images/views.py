# PACKAGES
import os
from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from urllib.parse import urlparse
from werkzeug import secure_filename
# USER-DEFINED MODULES
from app import app
from config import S3_BUCKET
from instagram_web.blueprints.images.helpers import *
from models.user import User

images_blueprint = Blueprint("images", __name__, template_folder='templates')


@images_blueprint.route("/new", methods=["GET"])
@login_required
def new():
    user = User.get_by_id(current_user.id)
    img = user.profile_image_url
    return render_template("images/new.html", img=img)


@images_blueprint.route("/", methods=["POST"])
@login_required
def create():
    if "user_file" not in request.files:
        flash("No user_file key in request.files")
        return redirect(url_for("images.new"))

    file = request.files["user_file"]

    if file.filename == "":
        flash("Please provide a file name")
        return redirect(url_for("images.new"))

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        print(str(output))
        url = urlparse(output).path.split('/')[-1]
        # Save to database
        q = User.update(profile_picture=url).where(User.id == current_user.id)

        if not q.execute():
            flash("an error occurred")
            return redirect(url_for("images.new"))
        flash("uploaded successfully")
    return redirect(url_for("images.new"))
