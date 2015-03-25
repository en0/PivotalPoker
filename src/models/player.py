__author__ = 'en0'

from models.generic_document import GenericDocumentFactory

# A player will join a game by posting the active game with the password (if needed)
# The path will add the player id and name from the users session.
# the system will validate the password if needed
# the system will push the new player to the joiner queue that will get picked up by the game worker thread.
# the game worker thread will add the player to the game.

Player = GenericDocumentFactory("PokerPlayer", [
    # Name,       Req,   Pub
    ('game_id',   True,  True),
    ('player_id', True,  False),
    ('name',      True,  True),
])
