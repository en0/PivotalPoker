__author__ = 'en0'

import pickle
from datetime import timedelta
from uuid import uuid4
from flask.sessions import SessionInterface
from exts.redis_session import RedisSession


class RedisSessionInterface(SessionInterface):
    def __init__(self, redis, prefix='session:', serializer=None, session_class=None):
        self.redis = redis
        self.prefix = prefix
        self.serializer = serializer or pickle
        self.session_class = session_class or RedisSession

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)

        # Store session ID
        #session['__sid__'] = session.sid

        # Store session
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val, int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)

