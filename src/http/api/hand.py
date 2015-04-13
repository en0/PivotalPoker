__author__ = 'en0'

from http import app, ApiException, context, request
from http.api.resource_base import ResourceBase, register_route
import models
import utils


class Hand(ResourceBase):
    __uri__ = '/api/v0.1/hand/'
    __pk__ = 'game_id'
    __pk_type__ = 'string'
    __method_hints__ = ['PUT', 'DELETE']

    @utils.enqueue
    def put(self, game_id):
        _game = models.Game.load(game_id, db=context.db)
        if not _game:
            raise ApiException('Not Found', 404)
        elif _game.owner_id != context.user.player_id:
            raise ApiException('Forbidden', 403)
        elif _game.current_hand is not None:
            raise ApiException('Conflict', 409)

        _hand = models.Hand(request.get_json())
        return models.QueueItem(game_id, _hand)

    @utils.enqueue
    def delete(self, game_id):
        _game = models.Game.load(game_id, db=context.db)
        if not _game:
            raise ApiException('Not Found', 404)
        elif _game.owner_id != context.user.player_id:
            raise ApiException('Forbidden', 403)
        elif _game.current_hand is None:
            raise ApiException('Conflict', 409)

        _request = models.WorkerRequest({
            'request_by': context.user.player_id,
            'action': 'abort_hand',
            'params': None
        })
        return models.QueueItem(game_id, _request)


register_route(Hand, app)
