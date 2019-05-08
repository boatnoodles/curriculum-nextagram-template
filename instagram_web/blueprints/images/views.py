# PACKAGES
import os
from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
# USER-DEFINED MODULES
from app import app
from config import S3_BUCKET
from instagram_web.blueprints.helpers import *
from models.user import User

profile_images_blueprint = Blueprint(
    "images", __name__, template_folder='templates')


@profile_images_blueprint.route("/new", methods=["GET"])
@login_required
def new():
    user = User.get_by_id(current_user.id)
    img = user.profile_image_url
    return render_template("images/new.html", img=img)


@profile_images_blueprint.route("/", methods=["POST"])
@login_required
def create():
    file = handle_file("user_file", "images")
    url = return_url(file)

    # Save to database
    q = User.update(profile_picture=url).where(User.id == current_user.id)

    if not q.execute():
        flash("an error occurred")
        return redirect(url_for("images.new"))

    flash("uploaded successfully")
    return redirect(url_for("images.new"))
