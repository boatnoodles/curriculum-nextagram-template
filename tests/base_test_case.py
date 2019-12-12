import inspect
import json
import os
from unittest import TestCase

import peewee
from flask import Flask
from flask_login import LoginManager

import config
from instagram_web.blueprints.users.views import users_blueprint
from models.post import Post
from models.user import User



class BaseTestCase(TestCase):
    def create_app(self):
        web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instagram_web')

        app = Flask('NEXTAGRAM', root_path=web_dir)

        app.config.from_object('config.TestingConfig')

        self._setup_login_manager(app)

        app.register_blueprint(users_blueprint, url_prefix="/users")

        @app.route("/")
        def home():
            return "temp work"

        return app

    
    def _setup_login_manager(self, app):
        login_manager = LoginManager()

        login_manager.login_view = "sessions.new"

        @login_manager.user_loader
        def get_user(id):
            user = User.get_by_id(id)
            return user

        login_manager.init_app(app)

    def setUp(self):
        self.app = self.create_app()

        # Required to make a request to own application
        self.client = self.app.test_client()

        # To activate request context temporarily, read more here https://github.com/jarus/flask-testing/blob/master/flask_testing/utils.py
        self._ctx = self.app.test_request_context()
        self._ctx.push()
    
    @classmethod
    def setUpClass(cls):
        os.system('dropdb nextagram_testing')

        os.system('createdb nextagram_testing')

        from database import db

        cls.db = db
        cls.db.create_tables([Post, User])

    @classmethod
    def tearDownClass(cls):
        cls.db.close()