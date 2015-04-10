__author__ = 'en0'

from unittest import TestCase
from time import time
import http
import json


class TestGame(TestCase):
    def setUp(self):
        http.app.config['REDIS_HOST'] = 'localhost'
        http.app.config['REDIS_DB'] = 1
        self.app = http.app.test_client()

    def register_session(self, player_name=None):
        if player_name is None:
            player_name = "unit test: {0}".format(str(int(time())))
        data = dict(name=player_name)
        self.app.put('/api/v0.1/session', data=json.dumps(data), content_type='application/json')

    def test_unauthorized(self):
        data = {
            "title": "Unit Test Game",
            "desc": "This game was created by the unit test",
            "pts_scale": [1, 2, 3, 5, 8]
        }
        rv = self.app.post('/api/v0.1/game/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(rv.status_code, 401)

    def test_all(self):
        data = {
            "title": "Unit Test Game",
            "desc": "This game was created by the unit test",
            "pts_scale": [1, 2, 3, 5, 8]
        }

        _expected = dict(current_hand=None, desc="This game was created by the unit test",
                         hands=[], owner_name="unit test", players={},
                         pts_scale=[1, 2, 3, 5, 8], state="Open", title="Unit Test Game", total_pts=0)

        self.register_session("unit test")

        # Create Game
        rv = self.app.post('/api/v0.1/game/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        _json = json.loads(rv.data)
        game_id = _json.get('game_id')
        self.assertDictContainsSubset(_expected, _json)
        self.assertEqual(_json.get('password'), None)
        self.assertIsNotNone(_json.get('game_id'))
        self.assertIsNotNone(_json.get('owner_id'))

        # Check if in the game list
        rv = self.app.get('/api/v0.1/game/')
        self.assertEqual(rv.status_code, 200)
        _json = json.loads(rv.data)
        _found_it = False
        for _game_entity in _json.get('games'):
            _found_it |= _game_entity['game_id'] == game_id
        self.assertTrue(_found_it)

        # Check game/{game_id}
        rv = self.app.get('/api/v0.1/game/{0}'.format(game_id))
        self.assertEqual(rv.status_code, 200)
        _json = json.loads(rv.data)
        self.assertDictContainsSubset(_expected, _json)

        # Delete game
        rv = self.app.delete(
            '/api/v0.1/game/{0}'.format(game_id),
            content_type='application/json'
        )
        self.assertEqual(rv.status_code, 204)
