__author__ = 'en0'


from flask import jsonify
from http import app, context, session, ApiException
from exts import Redis, RedisSessionInterface
from models import Session


redis = Redis(app)
app.session_interface = RedisSessionInterface(redis.connect())


@app.before_request
def request_init():
    context.db_connection = redis.connection

    if 'user' in session:
        context.user = Session.create(session['user'])
    else:
        context.user = None

@app.errorhandler(ApiException)
def api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
