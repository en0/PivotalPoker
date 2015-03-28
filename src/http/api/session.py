__author__ = 'en0'

from http import app, request, session, context, ApiException
from http.api.resource_base import ResourceBase, register_route
import models


class Session(ResourceBase):
    __uri__ = '/api/v0.1/session'
    __method_hints__ = ['GET', 'PUT']

    def get(self):
        if context.user:
            return context.user.entity
        raise ApiException("Not Found", status_code=404, payload={
            'help': "You must register a session first."
        })

    def put(self):
        json = request.get_json()
        new_session = models.Session.create(json=json)
        new_session.player_id = str(new_session.uuid)
        if context.user:
            new_session.player_id = context.user.player_id
        session['user'] = new_session.__document__
        return None, 201, {'Location': '/api/v0.1/session'}

register_route(Session, app)
