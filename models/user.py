from config import AWS_DOMAIN
from flask import flash, redirect, url_for
from flask_login import UserMixin
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
import peewee as pw
from werkzeug.security import generate_password_hash


class User(BaseModel, UserMixin):
    username = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.TextField(null=False)
    privacy = pw.BooleanField(default=False)
    profile_picture = pw.CharField(default="155755729502")

    @classmethod
    def hash_password(self, new_password):
        self.password = generate_password_hash(
            new_password, method="pbkdf2:sha256", salt_length=8)

    @hybrid_property
    def profile_picture_url(self):
        """Call via instance
        e.g., user = User.get_by_id(current_user.id)
        e.g., user.profile_picture_url"""
        return f"{AWS_DOMAIN}/{self.profile_picture}"

    @hybrid_property
    def is_private(self):
        return self.privacy
