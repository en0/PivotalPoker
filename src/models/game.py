__author__ = 'en0'

from models.redis_document import RedisDocumentFactory
import copy

GameBase = RedisDocumentFactory('PokerGame', [
    # Name, Req, Pub
    ('owner_id', True, False),
    ('owner_name', True, True),
    ('title', True, True),
    ('desc', False, True),
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
        return super(Game, cls).create(json, db=db)

    @classmethod
    def list(cls, db):
        _db = db
        _games = []
        for game_id in _db.hkeys(cls.__document_namespace__):
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
        _ret = super(Game, self).private_entity
        _ret['game_id'] = self.uuid
        return _ret

    #def register_game(self):
    #    key = "{0}:active".format(self.__document_namespace__)
    #    self.__db__.lpush(key, self.uuid)

    def add_player(self, player_id=None, name=None, player=None):
        if player:
            player_id = player.player_id
            name = player.name
        if not self.__document__['players']:
            self.__document__['players'] = {}
        self.__document__['players'][player_id] = name
        self.__is_dirty__ = True

    def remove_player(self, player_id):
        if not self.__document__['players']:
            self.__document__['players'] = {}
        if player_id in self.__document__['players']:
            del self.__document__['players'][player_id]
            self.__is_dirty__ = True

    def cast_vote(self, vote):
        # verify hand and players
        if not self.__document__['current_hand'] or not self.__document__['players']:
            return

        # Get player name and verify player is in game
        _player_name = self.__document__['players'].get(vote.player_id)
        if not _player_name:
            return

        # Add the vote to the current hand
        self.current_hand['votes'][vote.player_id] = {
            'name': _player_name,
            'vote': vote.vote
        }

        # Check if hand is complete.
        _player_count = len(self.__document__['players'])
        _vote_count = len(self.current_hand['votes'])

        if _vote_count == _player_count:
            self.state = "Reviewing"

        self.__is_dirty__ = True

    def resetVote(self):
        # verify hand
        if not self.__document__['current_hand']:
            return

        self.current_hand['votes'] = {}
        self.state = "Playing"

    def complete_hand(self, points):
        # verify hand
        if not self.__document__['current_hand']:
            return

        # Move the current hand into the completed hands list and empty the current hand
        complete_hand = copy.deepcopy(self.__document__['current_hand'])
        complete_hand['points'] = points
        self.__document__['current_hand'] = None
        self.__document__['hands'].append(complete_hand)

        self.state = "Open"
