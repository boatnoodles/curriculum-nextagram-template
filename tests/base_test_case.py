import json
import os
from unittest import TestCase

import config


class BaseTestCase(TestCase):
    def create_app(self):
        web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instagram_web')

        app = Flask('NEXTAGRAM', root_path=web_dir)

        app.config.from_object('config.TestingConfig')

        self._setup_login_manager(app)

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