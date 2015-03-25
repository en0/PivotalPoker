__author__ = 'en0'

from models.generic_document import GenericDocumentFactory

Session = GenericDocumentFactory("Session", [
    # Name,       Req,   Pub
    ('player_id', False,  False),
    ('name',      True,  True)
])
