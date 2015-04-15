__author__ = 'en0'

from models.generic_document import GenericDocumentFactory

# Once all votes have been cast (all players have voted) the hand will be set to complete
# once all votes have been cast (all players have voted) the game will be set to review.

# the onwer can either post to accept, revote, or cancel. by posting the result with the following:
#  result, points
# The system will look up the game
# The system will validate the owner from the current users session
# the system will push the result to the result queue

Result = GenericDocumentFactory('PokerHandResult', [
    # Name,       Req,  Pub
    ('result',    True, False), # Choice [ 'Accept', 'Revote', 'Cancel' ]
    ('points',    False, True)
])
