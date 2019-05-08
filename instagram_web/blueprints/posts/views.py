from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from instagram_web.blueprints.helpers import *
from models.post import Post
from models.user import User


posts_blueprint = Blueprint("posts", __name__, template_folder="templates")


@posts_blueprint.route("/new", methods=["GET"])
@login_required
# Upload new post page
def new():
    return render_template("posts/new.html")


@posts_blueprint.route("/", methods=["POST"])
@login_required
# Handles post upload
def create():
    # Handle and upload the file submitted by the user to generate a url path
    url_path = handle_upload("user_post", "posts")

    # Obtain the caption of the picture uploaded
    caption = request.form.get("caption")

    # Save to database
    q = Post(user_id=current_user.id, pict_url=url_path, caption=caption)

    if q.save():
        flash("Upload successful")
        return redirect(url_for("posts.new"))
    return redirect(url_for("posts.new"))


@posts_blueprint.route("/<path>", methods=["GET"])
@login_required
def show(path):
    post = Post.get(Post.pict_url == path)
    url = post.post_url
    caption = post.caption
    return render_template("posts/show.html", url=url, caption=caption)
