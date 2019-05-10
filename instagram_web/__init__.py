from app import app
from authlib.flask.client import OAuth
from flask import flash, redirect, render_template, url_for
from flask_assets import Environment, Bundle
from flask_login import current_user
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.images.views import profile_images_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.util.helpers.google_oauth import oauth
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(profile_images_blueprint, url_prefix="/images")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(users_blueprint, url_prefix="/users")


oauth.init_app(app)


@app.route("/")
def home():
    flash("works", "success")
    try:
        username = current_user.username
    except:
        username = "Stranger"
    if not current_user:
        return redirect(url_for("users.new"))
    return render_template('home.html', username=username)


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
