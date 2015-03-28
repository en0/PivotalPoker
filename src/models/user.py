__author__ = 'en0'

from models.generic_document import GenericDocumentFactory
from uuid import uuid4

UserBase = GenericDocumentFactory("User", [
    # Name,       Req,   Pub
    ('player_id', False,  False),
    ('name',      True,  True)
])


class User(UserBase):
    @classmethod
    def load(cls, json):
        json['player_id'] = str(uuid4())
        return super(User, cls).load(json)
