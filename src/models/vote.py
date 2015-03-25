__author__ = 'en0'

from models.generic_document import GenericDocumentFactory

# A vote will be cast by a player posting to the game with the following data:
#  vote
# the system will fill in the game_id from path variable
# the system will add the player id from the current users session
# The system will lookup the game.
# the system will verify the game state ('playing')
# the system will verify the player membership
# The system will push the vote to the vote queue.

Vote = GenericDocumentFactory('PokerVote', [
    # Name,       Req,  Pub
    ('game_id',   True, True),
    ('player_id', True, False),
    ('vote',      True, True)
])
