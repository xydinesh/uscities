import unittest
import transaction

from pyramid import testing

from .models import DBSession

import json
import requests

class TestUsCitiesFunctional(unittest.TestCase):
    """Test class for cities rest api"""
    def test_get_tn(self):
        res = requests.get('http://localhost:6543/api/1/cities?state=TN')
        res = json.loads(res.text)
        self.assertEqual(len(res), 583)

    def test_get_co(self):
        res = requests.get('http://localhost:6543/api/1/cities?state=CO')
        res = json.loads(res.text)
        self.assertTrue(len(res) > 0)
        self.assertEqual(len(res), 416)

    def test_get_co_80202(self):
        res = requests.get('http://localhost:6543/api/1/cities?zip=80202')
        res = json.loads(res.text)
        self.assertTrue(len(res) > 0)
        self.assertEqual(len(res), 1)

    def test_get_co_zip_80227(self):
        res = requests.get('http://localhost:6543/api/1/cities?zip=80227')
        res = json.loads(res.text)
        self.assertTrue(len(res) > 0)
        self.assertEqual(len(res), 1)
