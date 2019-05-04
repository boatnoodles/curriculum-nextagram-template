from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.TextField(null=False)
    privacy = pw.BooleanField(default=False)
