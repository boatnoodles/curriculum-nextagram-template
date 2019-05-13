from config import AWS_DOMAIN
from flask import flash, redirect, url_for
from flask_login import UserMixin
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
import peewee as pw
from werkzeug.security import generate_password_hash

import pysnooper


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

    @classmethod
    def is_following(self, username):
        user = User.get(User.username == username)
        if self.id == user.id:
            return 'self'
        else:
            for row in user.fans:
                if self.id == row.fan_id:
                    return False
                return True

    @hybrid_property
    def profile_picture_url(self):
        """Call via instance
        e.g., user = User.get_by_id(current_user.id)
        e.g., user.profile_picture_url"""
        return f"{AWS_DOMAIN}/{self.profile_picture}"

    @hybrid_property
    def is_private(self):
        return self.privacy

    # Who is the user following
    @hybrid_property
    def following(self):
        from models.followerfollowing import FollowerFollowing as FF
        return (User
                .select()
                .join(FF, on=FF.idol_id)
                .where(FF.fan_id == self.id, FF.approved == True)
                .order_by(User.username))

    # Who are the user's followers (who are my fans?)
    @hybrid_property
    def followers(self):
        from models.followerfollowing import FollowerFollowing as FF
        return (User
                .select()
                .join(FF, on=FF.fan_id)
                .where(FF.idol_id == self.id, FF.approved == True)
                .order_by(User.username))
