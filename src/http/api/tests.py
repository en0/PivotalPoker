__author__ = 'en0'

from http import app, request, context, ApiException
from http.api.resource_base import ResourceBase, register_route
import models


class Tests(ResourceBase):
    __uri__ = "/api/v0.1/tests/"
    __pk__ = "some_id"
    __pk_type__ = "string"
    __method_hints__ = ['GET', 'POST', 'DELETE']

    @models.enqueue
    def get(self, some_id=None):
        """ Just testing the queueing idea """
        if not some_id: return {}
        return models.QueueItem.load({
            'queue': 'join',
            'queue_id': some_id,
            'data': context.user.__document__
        })

    def post(self, some_id=None):
        return {}

    def delete(self, some_id=None):
        return {}


register_route(Tests, app)
