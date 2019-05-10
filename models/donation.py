import peewee as pw
from models.base_model import BaseModel
from models.post import Post
from models.user import User


class Donation(BaseModel):
    donor = pw.ForeignKeyField(User, backref='donations')
    recipient_post = pw.ForeignKeyField(Post, backref='donations')
    amount = pw.DecimalField(default=0)
