import peewee as pw
from models.base_model import BaseModel
from models.user import User


class Following(BaseModel):
    # fan = followers
    fan = pw.ForeignKeyField(User, backref="fans")
    # idol = following
    idol = pw.ForeignKeyField(User, backref="idols")
