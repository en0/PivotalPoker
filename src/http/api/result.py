__author__ = 'en0'

from http import app, ApiException, context, request
from http.api.resource_base import ResourceBase, register_route
import models
import utils


class Result(ResourceBase):
    __uri__ = '/api/v0.1/result/'
    __pk__ = 'game_id'
    __pk_type__ = 'string'
    __method_hints__ = ['PUT']

    @utils.enqueue
    def put(self, game_id):
        _game = models.Game.load(game_id, db=context.db)
        if not _game:
            raise ApiException('Not Found', 404)
        elif _game.state != 'Reviewing':
            raise ApiException('Conflict', 409)
        elif context.user.player_id != _game.owner_id:
            raise ApiException('Forbidden', 403)

        _result = models.Result(json=request.get_json())
        return models.QueueItem(game_id, _result)


register_route(Result, app)
