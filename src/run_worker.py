#!/usr/bin/env python2

__author__ = 'en0'

from worker import Monitor
from signal import SIGINT, SIGTERM, signal

if __name__ == "__main__":

    # Create an instance of our game monitor
    monitor = Monitor()

    def _shutdown(a,b):
        print("Shutting down. This could take a moment.")
        monitor.stop()

    # Listen for shutdown requests
    signal(SIGINT, _shutdown)
    signal(SIGTERM, _shutdown)

    # Start monitor
    monitor()
