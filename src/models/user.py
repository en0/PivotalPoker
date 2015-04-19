__author__ = 'en0'

from http import session
from models.generic_document import GenericDocumentFactory
from uuid import uuid4

UserBase = GenericDocumentFactory("User", [
    # Name,       Req,   Pub
    ('player_id', False,  True),
    ('name',      True,  True)
])


class User(UserBase):
    def __init__(self, json=None, document=None):
        if json:
            json['player_id'] = str(session.sid)
        super(User, self).__init__(json=json, document=document)

    def apply(self):
        session['user'] = self.__document__

    @classmethod
    def current(cls):
        if 'user' in session:
            return cls(document=session['user'])
        return None
