from tribeshop.models import Yak, Tribe
from tribeshop.controller import app
from tribeshop.services import *
from mongoengine import connect, disconnect
import json
import unittest


class TestYak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.yak = Yak(name='TestName', age=4.5, sex='f')
        cls.tribe = Tribe(
            tribe=[
                {'name': 'Test1', 'age': 4, 'sex': 'f'},
                {'name': 'Test2', 'age': 8, 'sex': 'm'},
                {'name': 'Test3', 'age': 9.5, 'sex': 'f'}
            ],
            total_milk=10000,
            total_wool=1000
            )
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')
    
    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_Yak(self):
        self.yak.save()
        test_entry = json.loads(Yak.objects().first().to_json())
        self.assertEqual(test_entry.get('name'), 'TestName')
        self.assertEqual(test_entry.get('age'), 4.5)
        self.assertEqual(test_entry.get('sex'), 'f')

    def test_Tribe(self):
        self.tribe.save()
        test_entry = json.loads(Tribe.objects().first().to_json())
        fresh_tribe = test_entry.get('tribe')
        self.assertEqual(fresh_tribe[0].get('name'), 'Test1')
        self.assertEqual(fresh_tribe[0].get('age'), 4)
        self.assertEqual(fresh_tribe[0].get('sex'), 'f')
        self.assertEqual(fresh_tribe[1].get('name'), 'Test2')
        self.assertEqual(fresh_tribe[1].get('age'), 8)
        self.assertEqual(fresh_tribe[1].get('sex'), 'm')
        self.assertEqual(fresh_tribe[2].get('name'), 'Test3')
        self.assertEqual(fresh_tribe[2].get('age'), 9.5)
        self.assertEqual(fresh_tribe[2].get('sex'), 'f')
        self.assertEqual(test_entry.get('total_milk'), 10000)
        self.assertEqual(test_entry.get('total_wool'), 1000)
    
    def test_calculate_stocks(self):
        self.yak.save()
        test_entry = json.loads(Yak.objects().first().to_json())
        test_total_milk, test_total_wool, \
            test_last_age, test_age_last_shaved\
            = calculate_stocks(13, test_entry)
        self.assertEqual(int(test_total_milk), 472)
        self.assertEqual(test_total_wool, 1)
        self.assertEqual(int(test_last_age), 4)
        self.assertEqual(test_age_last_shaved, 4.5)

if __name__ == '__main__':
    unittest.main()