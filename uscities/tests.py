import unittest
import transaction

from pyramid import testing

from .models import DBSession

import json

def _initDB():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    from .models import (
        Base,
        City,
        )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        city = City(
            zip=37902, state='TN', city='Knoxville', lat=35.962516, lng=-83.920915
        )
        DBSession.add(city)


        city = City(
            zip=37919, state='TN', city='Knoxville', lat=35.924385, lng=-84.001468
        )
        DBSession.add(city)

        city = City(
            zip=37920, state='TN', city='Kimberlin Height', lat=35.922976, lng=-83.879793
        )
        DBSession.add(city)

        city = City(
            zip=37921, state='TN', city='Karns', lat=35.976297, lng=-83.982894
        )
        DBSession.add(city)

        city = City(
            zip=37922, state='TN', city='Concord', lat=35.877697, lng=-84.127332
        )
        DBSession.add(city)
    return DBSession

class TestUsCitiesRESTApi(unittest.TestCase):
    """Test class for cities rest api"""
    def setUp(self):
        from pyramid.paster import get_app
        from webtest import TestApp
        app = get_app('testing.ini')
        self.testapp = TestApp(app)
        self.session = _initDB()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_get_city_37921(self):
        res = self.testapp.get('/api/1/cities/37921')
        res = json.loads(res.text)
        self.assertEqual(res['state'], 'TN')
        self.assertEqual(res['city'], 'Karns')
        self.assertEqual(res['zip'], 37921)

    def test_get_cities_tn(self):
        res = self.testapp.get('/api/1/cities?state=TN')
        res = json.loads(res.text)
        self.assertEqual(len(res), 5)

    def test_get_cities_zip(self):
        res = self.testapp.get('/api/1/cities?zip=37919')
        res = json.loads(res.text)
        self.assertEqual(len(res), 1) 
        res = res[0]
        self.assertEqual(res['city'], 'Knoxville')
        self.assertEqual(res['state'], 'TN')
