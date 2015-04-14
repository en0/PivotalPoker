__author__ = 'en0'

from http import app, ApiException, context, request
from http.api.resource_base import ResourceBase, register_route
import models
import utils


class Vote(ResourceBase):
    __uri__ = '/api/v0.1/vote/'
    __pk__ = 'game_id'
    __pk_type__ = 'string'
    __method_hints__ = ['PUT', 'DELETE']

    @utils.enqueue
    def put(self, game_id):
        _game = models.Game.load(game_id, db=context.db)
        if not _game:
            raise ApiException('Not Found', 404)
        elif _game.state != 'Playing':
            raise ApiException('Conflict', 409)

        _vote = models.Vote(game_id, context.user.player_id, request.get_json())
        return models.QueueItem(game_id, _vote)

    @utils.enqueue
    def delete(self, game_id):
        _game = models.Game.load(game_id, db=context.db)
        if not _game:
            raise ApiException('Not Found', 404)
        elif _game.state != 'Playing':
            raise ApiException('Conflict', 409)

        _request = models.WorkerRequest({
            'request_by': context.user.player_id,
            'action': 'retract_vote',
            'params': None
        })
        return models.QueueItem(game_id, _request)


register_route(Vote, app)
