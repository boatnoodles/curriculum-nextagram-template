import peewee as pw
from models.base_model import BaseModel
from models.user import User


class Post(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="posts")
    pict_url = pw.CharField()
    caption = pw.TextField()
