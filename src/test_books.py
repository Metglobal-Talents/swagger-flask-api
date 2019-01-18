import os
import unittest
from server import connex_app


class BookTestCase(unittest.TestCase):

    def setUp(self):
        connex_app.app.testing = True
        self.app = connex_app.app.test_client()

    def tearDown(self):
        pass

    def test_all_books(self):
        rv = self.app.get("/api/books")
        status_code = rv.status_code
        assert status_code == 200


if __name__ == '__main__':
    unittest.main()
