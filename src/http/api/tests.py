__author__ = 'en0'

from http import app, request, context, ApiException
from http.api.resource_base import ResourceBase, register_route
import models

from redis import Redis
import pickle

class Tests(ResourceBase):
    __uri__ = "/api/v0.1/tests/"
    __pk__ = "some_id"
    __pk_type__ = "string"
    __method_hints__ = ['GET', 'POST', 'DELETE']

    def get(self, some_id=None):
        """ Just testing the queueing idea """
        db = context.db
        assert isinstance(db, Redis)
        _p = models.Player.trusted_load(context.user.__document__)
        _raw = pickle.dumps(_p.__document__)
        db.lpush("PokerGameQueue:cb0d22b1-84d6-44af-acef-55e667be9dd1:joins", _raw)
        return dict(message="OK", status="Queued"), 202

    def post(self, some_id=None):
        return {}

    def delete(self, some_id=None):
        return {}


register_route(Tests, app)
