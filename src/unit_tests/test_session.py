__author__ = 'en0'

from unittest import TestCase
import http
import json


class TestSession(TestCase):
    def setUp(self):
        http.app.config['REDIS_HOST'] = 'localhost'
        http.app.config['REDIS_DB'] = 1
        self.app = http.app.test_client()

    def test_get_404(self):
        rv = self.app.get('/api/v0.1/session')
        self.assertEqual(rv.status_code, 404)

    def test_put(self):
        data = dict(name="Player Name")
        rv = self.app.put('/api/v0.1/session', data=json.dumps(data), content_type='application/json')
        self.assertEqual(rv.status_code, 201)
        rv = self.app.get('/api/v0.1/session')
        _json = json.loads(rv.data)
        self.assertEqual(_json.get('name'), data['name'])

