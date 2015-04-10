__author__ = 'en0'

import pickle
from http.midware import redis
import gevent
from pprint import pprint as pp
import models


def decode_item(serial_string):
    try:
        d = pickle.loads(serial_string)
        return models.QueueItem(document=d)
    except KeyError as e:
        if type(d) is dict and d.get('job_id') is not None:
            _job = models.BackgroundJob.load(d.get('job_id'))
            if _job is not None:
                _job.status = 500
                _job.message = e.message
                _job.save()


class Game(object):
    def __init__(self, game_id):
        self._game_id = game_id
        self._queue = "PokerGame:{0}:queue".format(self._game_id)

    def reload(self):
        return models.Game.load(self._game_id)

    def __call__(self):
        _db = redis.connection

        _game_ids = _db.hkeys('PokerGame')
        print("waiting on queue: {0}".format(self._queue))

        while self._game_id in _game_ids:
            _val = _db.blpop(self._queue, timeout=10)

            if _val:
                _, v = _val
                _item = decode_item(v)
                _model = self.reload()
                self.process(_model, _item)

            gevent.sleep(0.1)
            _game_ids = _db.hkeys('PokerGame')

        print("Exiting: {0}".format(self._queue))

    def process(self, model, item):
        pass
