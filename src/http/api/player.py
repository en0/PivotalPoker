__author__ = 'en0'

from http import app, ApiException, context, request
from http.api.resource_base import ResourceBase, register_route
import models


class Player(ResourceBase):
    __uri__ = '/api/v0.1/player/<string:game_id>/'
    __pk__ = 'player_id'
    __pk_type__ = 'string'
    __method_hints__ = ['POST', 'DELETE']

    @models.enqueue
    def post(self, game_id):
        _game = models.Game.load(game_id)
        if not _game:
            raise ApiException('Not Found', 404)
        elif _game.state != 'Open':
            raise ApiException('Conflict', 409)

        _player = models.Player(context.user.player_id, context.user.name, request.get_json())
        return models.QueueItem(game_id, _player)

    @models.enqueue
    def delete(self, game_id, player_id):
        raise NotImplementedError("Untestable without worker thread")
        _game = models.Game.load(game_id)
        if not _game:
            raise ApiException('Not Found', 404)
        elif player_id != context.user.player_id and player_id != _game.owner_id:
            raise ApiException('forbidden', 403)

        _request = models.WorkerRequest({
            'request_by': context.user.player_id,
            'action': 'remove_player',
            'params': player_id
        })
        return models.QueueItem(game_id, _request)


register_route(Player, app)
