import peewee as pw
from playhouse.hybrid import hybrid_property
from models.base_model import BaseModel
from models.user import User


class FollowerFollowing(BaseModel):
    # fan = follower
    fan = pw.ForeignKeyField(User, backref="following")
    # idol = following/followee
    idol = pw.ForeignKeyField(User, backref="followers")
    approved = pw.BooleanField(default=False)

    # Is there really need for the sake of naming convention
    @hybrid_property
    def is_approved(self):
        return self.approved
