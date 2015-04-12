#!/usr/bin/env python2
__author__ = 'en0'

from redis import Redis
from worker import Game

if __name__ == "__main__":
    db = Redis()
    g = Game("d4960521-24fd-4a21-a64f-45647b6402df", db=db)
    g()
