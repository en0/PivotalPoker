__author__ = 'en0'

from flask import copy_current_request_context
from http import app, request, context, ApiException
from http.api.resource_base import ResourceBase, register_route
import gevent
import models
import worker


class Game(ResourceBase):
    __uri__ = "/api/v0.1/game/"
    __pk__ = "game_id"
    __pk_type__ = "string"
    __method_hints__ = ['GET', 'POST', 'DELETE']

    def get(self, game_id=None):
        if game_id:
            _game = models.Game.load(uuid=game_id)
            if _game is None:
                raise ApiException("Not Found", 404)
            _ret = _game.entity
        else:
            _ret = dict(games=models.Game.list())
        return _ret

    def post(self):
        _game = models.Game.create(context.user.player_id, context.user.name, request.get_json())
        _worker = worker.Game(_game.uuid)
        _game.save()

        @copy_current_request_context
        def task():
            _worker()

        gevent.spawn(task)
        return _game.private_entity, 200, {'Location': '/api/v0.1/game/{0}'.format(_game.uuid)}

    def delete(self, game_id):
        _game = models.Game.load(uuid=game_id)

        if _game is None:
            raise ApiException("Not Found", 404)

        if str(_game.owner_id) == str(context.user.player_id):
            _game.delete()
        else:
            raise ApiException("Forbidden", 403)

        return None, 204


register_route(Game, app)
