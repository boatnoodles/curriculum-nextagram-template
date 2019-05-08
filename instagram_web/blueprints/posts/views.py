from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from instagram_web.blueprints.helpers import *
from models.post import *


posts_blueprint = Blueprint("posts", __name__, template_folder="templates")


@posts_blueprint.route("/new", methods=["GET"])
@login_required
# Upload new post page
def new():
    return render_template("posts/new.html")


@posts_blueprint.route("/", methods=["POST"])
# Handles post upload
@login_required
def create():
    # Handle and upload the file submitted by the user to generate a url
    file = handle_file("user_post", "posts")
    url = return_url(file)

    # Obtain the caption of the picture uploaded
    caption = request.form.get("caption")

    # Save to database
    q = Post(user_id=current_user.id, pict_url=url, caption=caption)

    if q.save():
        flash("Upload successful")
        return redirect(url_for("posts.new"))
    return redirect(url_for("posts.new"))
