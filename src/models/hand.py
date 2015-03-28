__author__ = 'en0'

from models.generic_document import GenericDocumentFactory

# A hand will be delt by the owner posting to the hand with the following data:
# body.
# The game id will be pulled from the route data.
# The system will lookup the game.
# the system will validate the owner of the game with the current users session.
# the system will fill the pts_scale with the game's pts_Scale.
# the system will fill the votes with the players from the game
# the system will push the hand into the hand queue

HandBase = GenericDocumentFactory('PokerHand', [
    # Name,         Req,  Pub
    ('game_id', True, True),
    ('body', True, True),
    ('votes', True, True),  # dict { 'uuid': { 'name' : 'Player Name', 'vote' : None } }
    ('complete', True, True),
])


class Hand(HandBase):
    def __init__(self, game_id=None, json=None, document=None):
        if document:
            _json = None
        elif game_id is None:
            raise KeyError()
        else:
            _json = json
            _json['game_id'] = game_id
            _json['votes'] = {}
            _json['complete'] = False

        super(Hand, self).__init__(json=_json, document=document)
