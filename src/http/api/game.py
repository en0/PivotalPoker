__author__ = 'en0'

from http import app, request, context, ApiException
from http.api.resource_base import ResourceBase, register_route
import models


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
            _ret['game_id'] = _game.uuid
        else:
            _ret = dict(games=models.Game.list())
        return _ret

    def post(self):
        json = request.get_json()

        # Can we move this into the model definition?
        json['owner_id'] = context.user.player_id
        json['owner_name'] = context.user.name
        json['players'] = {}
        json['hands'] = []
        json['current_hand'] = None
        json['total_pts'] = 0
        json['state'] = 'Open'

        _game = models.Game.create(json=json)
        _game.save()
        _ret = _game.private_entity
        _ret['game_id'] = _game.uuid
        return _ret, 200, {'Location': '/api/v0.1/game/{0}'.format(_game.uuid)}

    def delete(self, game_id):
        _game = models.Game.load(uuid=game_id)

        if _game is None:
            raise ApiException("Not Found", 404)

        if _game.owner_id == context.user.player_id:
            _game.delete()
        else:
            raise ApiException("Forbidden", 403)

        return None, 204


register_route(Game, app)
