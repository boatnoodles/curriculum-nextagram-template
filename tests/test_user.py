from flask import url_for

from models.user import User

from .base_test_case import BaseTestCase


class UserTestCase(BaseTestCase):
    def test_user_creation(self):
        form_data = {
            "username": "testing",
            "email": "testing@mail.com",
            "password": "!Aa123",
            "confirm": "!Aa123"
        }

        self.client.post(url_for('users.create'), data=form_data)

        user = User.select().where(User.username=="testing")

        self.assertTrue(user[0])