__author__ = 'en0'

from functools import wraps
from http import context, ApiException


def require_session(fn):

    @wraps(fn)
    def _wrap(*args, **kwargs):
        if context.user:
            return fn(*args, **kwargs)
        else:
            raise ApiException('Unauthorized', 401)
    return _wrap
