__author__ = 'en0'

from redis import Redis
from http import context
from functools import wraps
import models
import pickle


def enqueue(fn):

    @wraps(fn)
    def _wrapper(*args, **kwargs):
        # Expect a queue_item from the wrapped function
        queue_item = fn(*args, **kwargs)
        assert isinstance(queue_item, models.QueueItem)

        # Each job has a queue, use the queue_id to access it.
        _key = "PokerGame:{0}:queue".format(queue_item.queue_id)

        _db = context.db
        assert isinstance(_db, Redis)

        # Create a background entry to track this enqueue item
        _job = models.BackgroundJob.create(202)
        queue_item.job_id = _job.job_id
        _db.lpush(_key, pickle.dumps(queue_item.__document__))

        return _job.save_and_send()
    return _wrapper
