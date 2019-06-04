from app import app
from authlib.flask.client import OAuth
from flask import abort, flash, redirect, render_template, request, url_for
from flask_assets import Environment, Bundle
from flask_login import current_user
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.followings.views import followings_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.images.views import profile_images_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.util.helpers.oauth import google_oauth, facebook_oauth
from instagram_web.util.helpers.pagination import *
from models.followerfollowing import FollowerFollowing as FF
from models.post import Post
from models.user import User
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followings_blueprint, url_prefix="/followings")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(profile_images_blueprint, url_prefix="/images")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(users_blueprint, url_prefix="/users")


google_oauth.init_app(app)
facebook_oauth.init_app(app)


@app.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("users.new"))

    # Display only posts that are posted by current_user's approved idols
    posts = Post.select(Post, User.username).join(
        User).join(FF, on=FF.idol_id).where(FF.fan_id == current_user.id, FF.approved == True)

    # Create a pagination object from
    pages = Pagination(posts)
    current_page = request.args.get("page", default=1, type=int)
    # If the page number that is being accessed is invalid, return 404
    if current_page > pages.total_pages:
        abort(404)

    return render_template('home.html', pages=pages, current_page=current_page, posts=pages.items)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def access_denied(e):
    return render_template('403.html'), 403


app.register_error_handler(403, access_denied)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)
