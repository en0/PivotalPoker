#!/usr/bin/env python2
__author__ = 'en0'

from redis import Redis
from worker import Game

if __name__ == "__main__":
    db = Redis()
    # Clearly this is not going to work. we will need to have a monitor thread that spawns a new game worker
    # once a game starts.  We also need this monitor thread to boot strap all open games. This will give the
    # system a way to recover if the monitor and or worker thread crashes and needs to be restarted.

    # But for now, just replace the gameId with the game you are debugging with.
    # also, steal session: 8ee4f8f2-2255-4890-9874-3041815c6ca1
    game_worker = Game("d4960521-24fd-4a21-a64f-45647b6402df", db=db)
    game_worker()
