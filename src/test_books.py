import os
import unittest
import json
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

    def test_update_book(self):
        data = {"book_name": "835 Satır", "author_name": "Nazım Hikmet",
                "genre": "Şiir", "count": 100, "publish_date": "2000",
                "ISBN": "string"}
        rv = self.app.put("/api/books",
                          data=json.dumps(data),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 200

    def test_update_not_found(self):
        data = data = {"book_name": "It", "author_name": "Stephen King",
                        "genre": "Horror", "count": 100,
                        "publish_date": "1986", "ISBN": "asdf"}
        rv = self.app.put("/api/books",
                          data=json.dumps(data),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 404

    def test_update_missing_fields(self):
        data = data = {"book_name": "It", "author_name": "Stephen King",
                        "genre": "Horror", "count": 100,
                        "publish_date": "1986"}
        rv = self.app.put("/api/books",
                          data=json.dumps(data),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 400


if __name__ == '__main__':
    unittest.main()
