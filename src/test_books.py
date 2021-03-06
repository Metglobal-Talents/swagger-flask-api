import unittest
import json
from server import connex_app
import uuid


class BookTestCase(unittest.TestCase):

    def setUp(self):
        connex_app.app.testing = True
        self.app = connex_app.app.test_client()

    def tearDown(self):
        pass

    def create_isbn(self):
        code = str(uuid.uuid4().hex)[:13]
        rv = self.app.get("/api/books?ISBN=" + code)
        status_code = rv.status_code
        if status_code == 404:
            return code
        else:
            self.create_isbn()

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


    def test_reserve_book(self):
        data = {"ISBN": "9788700760356", "reservation_count": 1}
        rv = self.app.post("/api/library/reserve",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json"
                })

        status_code = rv.status_code
        assert status_code == 201

    def test_unsucces_reserve_book(self):
        data = {"ISBN": "9781523480501", "reservation_count": 2}
        rv = self.app.post("/api/library/reserve",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                })

        status_code = rv.status_code
        assert status_code == 404

    def test_too_much_reservation(self):
        data = {"ISBN": "9781523480500", "reservation_count": 100000}
        rv = self.app.post("/api/library/reserve",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                })

        status_code = rv.status_code
        assert status_code == 400

    def test_reservation_isbn_not_found_in_request_data(self):
        data = {"reservation_count": 1}
        rv = self.app.post("/api/library/reserve",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                })
        status_code = rv.status_code
        assert status_code == 404


    def test_update_book(self):
        data = {"book_name": "835 Satır", "author_name": "Nazım Hikmet",
                "genre": "Şiir", "count": 100, "publish_date": "2000",
                "ISBN": "9780007203550"}
        rv = self.app.put("/api/books",
                          data=json.dumps(data),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 200

    def test_update_not_found(self):
        data = {"book_name": "It", "author_name": "Stephen King",
                       "genre": "Horror", "count": 100,
                       "publish_date": "1986", "ISBN": "asdf"}
        rv = self.app.put("/api/books",
                          data=json.dumps(data),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 404

    def test_update_missing_fields(self):
        data = {"book_name": "It", "author_name": "Stephen King",
                       "genre": "Horror", "count": 100,
                       "publish_date": "1986"}
        rv = self.app.put("/api/books",
                          data=json.dumps(data),
                          headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 400

    def test_create_already_exists(self):
        rv = self.app.get("/api/books")
        book = rv.json[0]
        data = {
            "book_name" : book.get("book_name"),
            "author_name" : book.get("author_name"),
            "genre" : book.get("genre"),
            "ISBN" : book.get("ISBN"),
            "count" : book.get("count"),
            "reservation_count" : book.get("reservation_count")
        }
        rv = self.app.post("/api/books", data=json.dumps(data),
                           headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 400

    def test_create_success(self):
        data = {"ISBN": self.create_isbn(), "book_name": "It", "author_name": "Stephen King",
                "genre": "Horror", "count": 100, "publish_date": "1986"}
        rv = self.app.post("/api/books", data=json.dumps(data),
                           headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 201

    def test_create_unsuccess(self):
        data = {"ISBN": 1313, "book_name": "It",
                "author_name": "Stephen King",
                "genre": "Horror", "count": 100, "publish_date": "1986-01-01"}
        rv = self.app.post("/api/books", data=json.dumps(data),
                           headers={"Content-Type": "application/json"})
        status_code = rv.status_code
        assert status_code == 400

    def test_borrow_book_success(self):
        data = {"ISBN": "9781408835005", "reservation_count": 10}
        rv = self.app.post("/api/library/reserve",
                           data=json.dumps(data),
                           headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        res = rv.json
        reserv_id = res["reservation_id"]
        data_borrow = {"reservation_id": reserv_id}
        rv1 = self.app.put("/api/library/borrow",
                            data=json.dumps(data_borrow),
                            headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        status_code = rv1.status_code
        assert status_code == 200

    def test_borrow_book_unsuccess(self):
        data = {"ISBN": "9781408812335005", "reservation_count": 10}
        rv = self.app.put("/api/library/borrow",
                            data=json.dumps(data),
                            headers={"Content-Type": "application/json",
                                    "Accept": "application/json"})
        status_code = rv.status_code
        assert status_code == 404

    def test_return_books_bad_request(self):
        data = {"reservation_id": 10}
        rv = self.app.put("/api/library/return",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json"
                })
        status_code = rv.status_code
        assert status_code == 400

    def test_return_books_not_found(self):
        data = {"reservation_id": "asdasdasd"}
        rv = self.app.put("/api/library/return",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json"
                })
        status_code = rv.status_code
        assert status_code == 404

    def test_return_books_success(self):
        data = {"ISBN": "9788700760356", "reservation_count": 1}
        rv = self.app.post("/api/library/reserve",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json"
                })
        reservation_id = rv.json.get("reservation_id")
        data = {"reservation_id": reservation_id}
        rv = self.app.put("/api/library/return",
                data=json.dumps(data),
                headers={
                        "Content-Type": "application/json"
                })
        status_code = rv.status_code
        assert status_code == 200

        
if __name__ == '__main__':
    unittest.main()
