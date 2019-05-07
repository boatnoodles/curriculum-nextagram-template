from app import login_manager
from flask_login import UserMixin
from models.base_model import BaseModel
import peewee as pw


@login_manager.user_loader
def get_user(id):
    user = User.get_by_id(id)
    return user


class User(BaseModel, UserMixin):
    username = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.TextField(null=False)
    privacy = pw.BooleanField(null=True, default=False)
    profile_picture = pw.CharField(null=True, default=None)
    # TODO SET DEFAULT PICTURE

    # @pw.hybrid_property
    # def profile_image_url(self):
    #     profile_pic = self.images.where(self.as)
    #     return f"http://{bucket_name}.s3.amazonaws.com/{self.profile_picture}"

    #     https
