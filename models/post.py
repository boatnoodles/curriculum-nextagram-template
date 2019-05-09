# Packages
import peewee as pw
from playhouse.hybrid import hybrid_property
# User-defined modules
from config import AWS_DOMAIN
from models.base_model import BaseModel
from models.user import User


class Post(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="posts")
    path = pw.CharField()
    caption = pw.TextField()
    donation = pw.DecimalField(default=0)

    @hybrid_property
    def post_url(self):
        return f"{AWS_DOMAIN}/{self.path}"

    @hybrid_property
    def donation_amount(self):
        return
