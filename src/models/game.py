__author__ = 'en0'

from models.redis_document import RedisDocumentFactory

# To start a game -
# Post a game with title, description, pts_scale, and password (optional)
# The game will add an emtpy dict for players, empty array for hands, 0 total_pts, set owner_id, set state to Open
# The game will add current_hand to None
# Document will be saved with expiration in 3 hrs.
# The system will start a game worker thread.
# - If state is open, the worker thread pulls from the joiner queue and the hand queue
#   -  When a hand is received, the current hand is set and the state is changed to playing
#   - If state is playing, the worker thread will pull from the vote queue and the abort queue.
#   -  When a abort is recieved, process:
#       ACTION: abort game - delete the game, kill the worker thread
#       ACTION: abort hand - ** see ACTION cancel in result queue
#   - If state is reviewing, the worker thread will listen to the result queue
#   -  When a result is recieved, the current hand will be processed:
#       ACTION: accept - move hand to hands. increment points, set game state to Open
#       ACTION: revote - Empty votes in current hand, set hand complete state to false, set game state to playing
#       ACTION: cancel - delete current hand, set state to Open
# The game will be sent back with the SID

GameBase = RedisDocumentFactory('PokerGame', [
    # Name, Req, Pub
    ('owner_id', True, False),
    ('owner_name', True, True),
    ('title', True, True),
    ('desc', True, True),
    ('players', True, True),  # dict { 'uuid': 'Player Name' }
    ('hands', True, True),
    ('current_hand', True, True),  # See Hand
    ('total_pts', True, True),
    ('pts_scale', True, True),
    ('state', True, True),  # Choice [ 'Open', 'Playing', 'Reviewing' ]
    ('password', False, False),  # optional to protect joining
])


class Game(GameBase):

    @classmethod
    def create(cls, owner_id, owner_name, json, db):
        json['owner_id'] = owner_id
        json['owner_name'] = owner_name
        json['players'] = {}
        json['hands'] = []
        json['current_hand'] = None
        json['total_pts'] = 0
        json['state'] = 'Open'
        super(Game, cls).create(json, db=db)

    @classmethod
    def list(cls, db):
        _games = []
        for game_id in db.hkeys(cls.__document_namespace__):
            _game = super(Game, cls).load(game_id, db=db)
            if _game.state == 'Open':
                _games.append({
                    'title': _game.title,
                    'game_id': _game.uuid,
                    'owner_name': _game.owner_name,
                    'has_password': _game.password is not None
                })
        return _games

    @property
    def entity(self):
        _ret = super(Game, self).entity
        _ret['game_id'] = self.uuid
        return _ret

    @property
    def private_entity(self):
        _ret = super(Game, self).entity
        _ret['game_id'] = self.uuid
        return _ret

    def add_player(self, player_id=None, name=None, player=None):
        if player:
            player_id = player.player_id
            name = player.name
        if not self.__document__['players']:
            self.__document__['players'] = {}
        self.__document__['players'][player_id] = name

    def remove_player(self, player_id):
        if not self.__document__['players']:
            self.__document__['players'] = {}
        if player_id in self.__document__['players']:
            del self.__document__['players'][player_id]
