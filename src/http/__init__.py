__author__ = 'ilaird'

from flask import Flask, g as context, session, abort, request
import config
from exts.exceptions import ApiException

app = Flask(__name__)
app.config.from_object(config.Default)

try:
    app.config.from_envvar('PIVOTALPOKER_CONFIG')
except RuntimeError:
    app.config.from_object(config.Debug)
    print("WARNING: No configuration file found!")
    print("Continuing in debug mode...")

import http.midware
import http.ui
import http.api

__all__ = [
    'app',
    'context',
    'session',
    'abort',
    'request',
    'ApiException'
]