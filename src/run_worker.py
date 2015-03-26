__author__ = 'en0'

import models
from redis import Redis
from threading import Thread
import pickle

#####################
# Proof of concept. #
#####################

def game_worker(game_id):
    db = Redis()
    queue_namespace = "PokerGameQueue:{0}".format(game_id)
    print(game_id)
    _vote_queue = "{0}:votes".format(queue_namespace)
    _join_queue = "{0}:joins".format(queue_namespace)

    _game_queues = db.hkeys('PokerGame')
    print('running', _game_queues)
    while game_id in _game_queues:

        _val = db.blpop(_join_queue)
        if _val:
            _, val = _val
            player = models.Player.trusted_load(pickle.loads(val))
            print("Got new player:", player.private_entity)

        _game_queues = db.hkeys('PokerGame')

    print('exited')


if __name__ == '__main__':
    db = Redis()
    while True:
        _val = db.blpop('PokerGameQueue', timeout=5)
        if _val:
            _, _v = _val
            t = Thread(target=game_worker, args=(_v,))
            print('Starting game thread:', t)
            t.start()
