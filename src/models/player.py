__author__ = 'en0'

from models.generic_document import GenericDocumentFactory

# A player will join a game by posting the active game with the password (if needed)
# The path will add the player id and name from the users session.
# the system will validate the password if needed
# the system will push the new player to the joiner queue that will get picked up by the game worker thread.
# the game worker thread will add the player to the game.

PlayerBase = GenericDocumentFactory("PokerPlayer", [
    # Name,       Req,   Pub
    ('player_id', True,  False),
    ('name',      True,  True),
    ('password',  False, False),
])


class Player(PlayerBase):
    def __init__(self, player_id=None, name=None, json=None, document=None):
        if document:
            _json = None
        elif player_id is None:
            raise KeyError()
        elif name is None:
            raise KeyError()
        else:
            _json = json
            _json['player_id'] = player_id
            _json['name'] = name

        super(Player, self).__init__(json=_json, document=document)
