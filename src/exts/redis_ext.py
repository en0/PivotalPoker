__author__ = 'ilaird'

from flask import current_app
from redis import Redis as RRedis

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Redis(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('REDIS_HOST', 'localhost')
        app.config.setdefault('REDIS_PORT', 6379)
        app.config.setdefault('REDIS_DB', 0)
        app.config.setdefault('REDIS_PASSWORD', '')
        app.config.setdefault('REDIS_SOCKET_TIMEOUT', None)
        app.config.setdefault('REDIS_CONNECTION_POOL', None)
        app.config.setdefault('REDIS_CHARSET', 'utf-8')
        app.config.setdefault('REDIS_ERRORS', 'strict')
        app.config.setdefault('REDIS_DECODE_RESPONSES', False)
        app.config.setdefault('REDIS_UNIX_SOCKET_PATH', None)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'redis_db'):
            ctx.redis_db.connection_pool.disconnect()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redis_db'):
                ctx.redis_db = self.connect()
            return ctx.redis_db

    def connect(self):
        return RRedis(
            host=self.app.config['REDIS_HOST'],
            port=self.app.config['REDIS_PORT'],
            db=self.app.config['REDIS_DB'],
            password=self.app.config['REDIS_PASSWORD'],
            socket_timeout=self.app.config['REDIS_SOCKET_TIMEOUT'],
            connection_pool=self.app.config['REDIS_CONNECTION_POOL'],
            charset=self.app.config['REDIS_CHARSET'],
            errors=self.app.config['REDIS_ERRORS'],
            decode_responses=self.app.config['REDIS_DECODE_RESPONSES'],
            unix_socket_path=self.app.config['REDIS_UNIX_SOCKET_PATH']
        )
