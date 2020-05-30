import unittest
from config import TestServerConfig
from app import app

class TestFlask(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health(self):
        res_stat = self.app.get('/healthcheck').status_code
        self.assertEqual(res_stat,200)

    def test_search(self):
        res_search = self.app.get('search/la').json
        self.assertEqual(res_search,
        {'la': ['ladies', 'last', 'lady', 'ladyship', 'large']})

if __name__ == '__main__':
    unittest.main()