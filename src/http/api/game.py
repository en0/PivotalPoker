
__author__ = 'en0'

from http import app, request, context, ApiException
from http.api.resource_base import ResourceBase, register_route
from utils import require_session
import utils
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

            if _game.owner_id == context.user.player_id:
                _ret = _game.private_entity
            else:
                _ret = _game.entity
        else:
            _ret = dict(games=models.Game.list(db=context.db))
        return _ret

    @require_session
    def post(self):
        _game = models.Game.create(context.user.player_id, context.user.name, request.get_json(), db=context.db)
        _game.save()
        return _game.private_entity, 200, {'Location': '/api/v0.1/game/{0}'.format(_game.uuid)}

    @utils.enqueue
    def delete(self, game_id):
        _game = models.Game.load(uuid=game_id, db=context.db)

        if _game is None:
            raise ApiException("Not Found", 404)

        if not str(_game.owner_id) == str(context.user.player_id):
            raise ApiException("Forbidden", 403)

        _request = models.WorkerRequest({
            'request_by': context.user.player_id,
            'action': 'close_game',
            'params': None
        })

        return models.QueueItem(game_id, _request)


register_route(Game, app)
