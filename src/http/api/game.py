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
            _game = models.Game.load(uuid=game_id, db=context.db)
            if _game is None:
                raise ApiException("Not Found", 404)
            _ret = _game.entity
        else:
            _ret = dict(games=models.Game.list(db=context.db))
        return _ret

    def post(self):
        _game = models.Game.create(context.user.player_id, context.user.name, request.get_json(), db=context.db)
        _game.save()
        return _game.private_entity, 200, {'Location': '/api/v0.1/game/{0}'.format(_game.uuid)}

    def delete(self, game_id):
        _game = models.Game.load(uuid=game_id, db=context.db)

        if _game is None:
            raise ApiException("Not Found", 404)

        if _game.owner_id == context.user.player_id:
            _game.delete()
        else:
            raise ApiException("Forbidden", 403)

        return None, 204


register_route(Game, app)
