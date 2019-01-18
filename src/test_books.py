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

    def test_book_search_by_book_name(self):
        rv = self.app.get("/api/books?book_name=ring")
        status_code = rv.status_code
        assert status_code == 200

    def test_book_search_by_author_name(self):
        rv = self.app.get("/api/books?author_name=tolkien")
        status_code = rv.status_code
        assert status_code == 200

    def test_book_search_by_genre(self):
        rv = self.app.get("/api/books?genre=fantazzzzzzzzziiiiii")
        status_code = rv.status_code
        assert status_code == 404

    def test_book_search_by_isbn(self):
        rv = self.app.get("/api/books?ISBN=9781408835005")
        status_code = rv.status_code
        assert status_code == 200

    def test_book_search_by_publish_date(self):
        rv = self.app.get("/api/books?publish_date=1954-01-01")
        status_code = rv.status_code
        assert status_code == 200

    def test_book_search_by_wrong_publish_date(self):
        rv = self.app.get("/api/books?publish_date=asdasdasdasd")
        status_code = rv.status_code
        assert status_code == 400

    def test_book_search_complex_query(self):
        rv = self.app.get("/api/books?book_name=lotr&publish_date=1955-01-01")
        status_code = rv.status_code
        assert status_code == 200

    def test_delete_success(self):
        data = {"ISBN": "9781408835005"}
        rv = self.app.delete("/api/books",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json",
                                      "Accept": "application/json"})
        status_code = rv.status_code
        assert status_code == 200

    def test_delete_unsuccess(self):
        data = {"ISBN": "9781408835"}
        rv = self.app.delete("/api/books",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json",
                                      "Accept": "application/json"})
        status_code = rv.status_code
        assert status_code == 404

if __name__ == '__main__':
    unittest.main()
