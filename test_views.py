import os
import shutil
import unittest
from flask import json

class NewsView(unittest.TestCase):
    def setUp(self):
        import web
        reload(web)
        self.app = web.app.test_client()

    def tearDown(self):
        try:
            shutil.rmtree('urlshortner')
        except:
            pass

    def test_get_home(self):
        response = self.app.get('/', follow_redirects=True)
        assert 200 == response.status_code
        assert 'Loogi.ca' in response.data
        assert 'input' in response.data

    def test_urls(self):
        response = self.app.get('/urls/')
        assert 200 == response.status_code
        assert {} == json.loads(response.data)

    def test_get_ranking(self):
        response = self.app.get('/ranking')
        assert 200 == response.status_code
        assert 'Ranking' in response.data

    def test_add_url(self):
        data = json.dumps(dict(url='http://loogi.ca'))
        response = self.app.post('/add_url/', data=data,
                                              content_type="application/json")
        assert 200 == response.status_code
        assert 'http://loogi.ca' == json.loads(response.data)['url']
        assert 'shortned' in json.loads(response.data)

    def test_add_invalid_url(self):
        data = json.dumps(dict(url='loogica'))
        response = self.app.post('/add_url/', data=data,
                                              content_type="application/json")
        assert 200 == response.status_code
        assert 'error' in json.loads(response.data)

    def test_resolved(self):
        data = json.dumps(dict(url='http://loogi.ca'))
        response = self.app.post('/add_url/', data=data,
                                              content_type="application/json")
        url_short_id = json.loads(response.data)['shortned']
        response = self.app.get('/%s' % url_short_id)

        assert 302 == response.status_code
        assert 'Location' in str(response.headers)
        assert 'http://loogi.ca' in str(response.headers)

    def test_bad_resolved(self):
        response = self.app.get('/invalid')
        assert 404 == response.status_code


