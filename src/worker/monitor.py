__author__ = 'en0'

from worker import Game
import config
import threading
import imp
from time import sleep, time
from os import getenv
from redis import Redis as RRedis
import models


def _extend_attrib(target, source):
    for attrib in [a for a in dir(source) if not a.startswith('__')]:
        target[attrib] = getattr(source, attrib)


def _load_config(config_environmental_variable):
    _config = {}
    _extend_attrib(_config, config.Default)
    try:
        _path = getenv(config_environmental_variable)
        if _path:
            custom_config = imp.load_source("CONFIG", _path)
            _extend_attrib(_config, custom_config)
        else:
            raise ImportError('no config')
    except IOError:
        raise IOError('Configuration file not found.')
    except ImportError:
        _extend_attrib(_config, config.Debug)
        print("WARNING: No configuration file found!")
        print("Continuing in debug mode...")

    return _config


def _get_db(**kwargs):
    kwargs.setdefault('REDIS_HOST', 'localhost')
    kwargs.setdefault('REDIS_PORT', 6379)
    kwargs.setdefault('REDIS_DB', 0)
    kwargs.setdefault('REDIS_PASSWORD', '')
    kwargs.setdefault('REDIS_SOCKET_TIMEOUT', None)
    kwargs.setdefault('REDIS_CONNECTION_POOL', None)
    kwargs.setdefault('REDIS_CHARSET', 'utf-8')
    kwargs.setdefault('REDIS_ERRORS', 'strict')
    kwargs.setdefault('REDIS_DECODE_RESPONSES', False)
    kwargs.setdefault('REDIS_UNIX_SOCKET_PATH', None)

    return RRedis(
        host=kwargs['REDIS_HOST'],
        port=kwargs['REDIS_PORT'],
        db=kwargs['REDIS_DB'],
        password=kwargs['REDIS_PASSWORD'],
        socket_timeout=kwargs['REDIS_SOCKET_TIMEOUT'],
        connection_pool=kwargs['REDIS_CONNECTION_POOL'],
        charset=kwargs['REDIS_CHARSET'],
        errors=kwargs['REDIS_ERRORS'],
        decode_responses=kwargs['REDIS_DECODE_RESPONSES'],
        unix_socket_path=kwargs['REDIS_UNIX_SOCKET_PATH']
    )


class Monitor():
    def __init__(self):
        self._config = _load_config('PIVOTALPOKER_CONFIG')
        self._db = _get_db(**self._config)
        self._threads = []
        self._event = threading.Event()

    def stop(self):
        self._event.set()

    def __call__(self):
        def _games_forever(db):
            while not self._event.is_set():
                for gid in Game.get_games(db):
                    yield Game(gid, db=db)

        for game in _games_forever(self._db):
            if game.is_game_worker_exist():
                new_thread = threading.Thread(target=game, args=(self._event,))
                self._threads.append(new_thread)
                new_thread.start()
                sleep(1)
            else:
                del game
                self._db_maintenance()
                sleep(5)

    def _db_maintenance(self):
        _now = int(time())
        for job_id in self._db.hkeys(models.BackgroundJob.__document_namespace__):
            _job = models.BackgroundJob.load(job_id, db=self._db)
            if (_now - _job.mtime) > 100:
                print("Removing expired key: {0}".format(job_id))
                self._db.hdel(models.BackgroundJob.__document_namespace__, job_id)
