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
@login_required
# Handles post upload
def create():

    return redirect(url_for("posts.new"))
