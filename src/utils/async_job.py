__author__ = 'en0'

from http import context
from uuid import uuid4
from redis import Redis
from gevent import spawn
from functools import wraps


class AsyncJob(object):
    def __init__(self, target):
        assert isinstance(context.db, Redis)
        self._target = target
        self._db = context.db

    def __call__(self, fn):
        wraps(fn)

        def _wrapper(*args, **kwargs):
            _args = fn(*args, **kwargs)

            _job_id = str(uuid4())
            _key = "jobs:{0}".format(_job_id)
            _status_key = "jobs:{0}:status".format(_job_id)
            _expire_time = 3600

            self._db.set(_status_key, 202)
            self._db.expire(_status_key, _expire_time)

            def task():
                # noinspection PyBroadException
                try:
                    data = self._target(*_args)
                except:
                    self._db.set(_status_key, 500)
                else:
                    self._db.set(_key, data)
                    self._db.set(_status_key, 200)
                    self._db.expire(_key, _expire_time)
                self._db.expire(_status_key, _expire_time)

            spawn(task)
            return dict(job=_job_id)

        return _wrapper
