import os
import json
import unittest
import tempfile
from server import app
from library import library


class BookTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_all_books(self):
        rv = self.app.get("/api/books")
        status_code = rv.status_code
        assert status_code == 200

    def test_rowling_books(self):
        rv = self.app.get("/api/books?author_name=J.K.+Rowling")
        status_code = rv.status_code
        assert status_code == 200

    def test_invalid_filter(self):
        rv = self.app.get("/api/books?x=1")
        status_code = rv.status_code
        assert status_code == 400

    def test_not_found(self):
        rv = self.app.get("/api/books?author_name=Tolga+Bilbey")
        status_code = rv.status_code
        assert status_code == 400

    def test_complex_search(self):
        rv = self.app.get(
            "/api/books?author_name=J.K.+Rowling&book_name=Harry+Potter+and+Prisoner+of+Azkaban")
        status_code = rv.status_code
        assert status_code == 200

    def test_create_success(self):
        data = {"book_name": "It", "author_name": "Stephen King",
                "genre": "Horror", "count": 100, "publish_date": "1986"}
        rv = self.app.post("/api/books/create", data=json.dumps(data),
                           headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 200

    def test_create_unsuccess(self):
        data = {"book_name": "It", "author_name": "Stephen King",
                "genre": "Horror", "count": 100, "publish_date": 1986}
        rv = self.app.post("/api/books/create", data=json.dumps(data),
                           headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 400

    def test_create_already_exists(self):
        data = library.books[0].to_json()
        rv = self.app.post("/api/books/create", data=json.dumps(data),
                           headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 406

    def test_update_book(self):
        data1 = {"book_name": "It", "author_name": "Stephen King",
                 "genre": "Horror", "count": 100, "publish_date": "1986"}
        rv = self.app.put("/api/books/update/9788324137930",
                          data=json.dumps(data1),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 200

    def test_update_not_found(self):
        data = library.books[0].to_json()
        rv = self.app.put("/api/books/update/97872050",
                            data=json.dumps(data),
                            headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 404

    def test_delete_success(self):
        rv = self.app.delete("/api/books/delete/9780007203550")
        status_code = rv.status_code
        assert status_code == 200

    def test_delete_unsuccess(self):
        rv = self.app.delete("/api/books/delete/123")
        status_code = rv.status_code
        assert status_code == 404

    def test_reserve_book_success(self):
        data = {"reservation_count": 10}
        rv = self.app.post("/api/library/reserve/9781408835005",
                           data=json.dumps(data),
                           headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        status_code = rv.status_code
        assert status_code == 200

    def test_reserve_book_unsuccess(self):
        data = {"reservation_count": 0}
        rv = self.app.post("/api/library/reserve/9781408835005",
                           data=json.dumps(data),
                           headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        status_code = rv.status_code
        assert status_code == 400

    def test_borrow_book_success(self):
        data = {"reservation_count": 10}
        rv = self.app.post("/api/library/reserve/9781408835005",
                           data=json.dumps(data),
                           headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        res = rv.json
        reserv_id = res["reservation_id"]
        rv1 = self.app.put("/api/library/borrow/" + reserv_id)
        status_code = rv1.status_code
        assert status_code == 200

    def test_borrow_book_unsuccess(self):
        rv1 = self.app.put("/api/library/borrow/123")
        status_code = rv1.status_code
        assert status_code == 404

    def test_return_book_success(self):
        data = {"reservation_count": 10}
        rv = self.app.post("/api/library/reserve/9781408835005",
                           data=json.dumps(data),
                           headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        json_rv = rv.json
        res_id = json_rv['reservation_id']
        rv_borrow = self.app.put("/api/library/borrow/" + res_id)
        rv_return = self.app.put('/api/library/return/' + res_id)
        status_code = rv_return.status_code
        assert status_code == 200

    def test_return_book_unsuccess(self):
        rv = self.app.put("/api/library/return/1123")
        status_code = rv.status_code
        assert status_code == 404


if __name__ == '__main__':
    unittest.main()
