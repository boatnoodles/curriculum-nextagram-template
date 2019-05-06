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
    privacy = pw.BooleanField(default=False)
