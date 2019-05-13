from app import login_manager
from config import AWS_DOMAIN
from flask_login import UserMixin
from models.base_model import BaseModel
# from models.relationship import FollowerFollowing
from playhouse.hybrid import hybrid_property
import peewee as pw
from werkzeug.security import generate_password_hash


@login_manager.user_loader
def get_user(id):
    user = User.get_by_id(id)
    return user


login_manager.login_view = "sessions.new"


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
        return True if self.privacy else False

    # Who is the user following (who are my idols?)
    # @classmethod
    # def idols(self):
    #     return (User
    #             .select()
    #             .join(FollowerFollowing, on=FollowerFollowing.to_user)
    #             .where(FollowerFollowing.from_user == self)
    #             .order_by(User.username))

    # # Who are the user's followers (who are my fans?)
    # @classmethod
    # def fans(self):
    #     return (User
    #             .select()
    #             .join(FollowerFollowing, on=FollowerFollowing.from_user)
    #             .where(FollowerFollowing.to_user == self)
    #             .order_by(User.username))

    # # Follow someone
    # def follow(self, user):
    # # Unfollow someone
    # def unfollow(self, user):
