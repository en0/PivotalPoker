__author__ = 'en0'

import pickle
from http.midware import redis
import gevent
from pprint import pprint as pp


## This could use some data abstraction


class Game(object):
    def __init__(self, game_id):
        self._game_id = game_id
        self._queue = "PokerGame:{0}:queue".format(self._game_id)

    def __call__(self):
        _db = redis.connection

        _game_ids = _db.hkeys('PokerGame')
        print("waiting on queue: {0}".format(self._queue))
        while self._game_id in _game_ids:
            _val = _db.blpop(self._queue, timeout=10)

            if _val:
                _, v = _val
                print("Do something with this:")
                pp(pickle.loads(v))

            gevent.sleep(0.1)
            _game_ids = _db.hkeys('PokerGame')
