from flask import request, abort
from models import Book, BookSchema, Reservation, ReservationSchema, db
from datetime import datetime
import uuid

books_schema = BookSchema(many=True)
book_schema = BookSchema()
reservations_schema = ReservationSchema(many=True)
reservation_schema = ReservationSchema()


def search():
    book_name = request.args.get('book_name', '')
    author_name = request.args.get('author_name', '')
    genre = request.args.get('genre', '')
    ISBN = request.args.get('ISBN', '')
    publish_date = request.args.get('publish_date')

    books = Book.query.filter(
        (Book.book_name.ilike('%{}%'.format(book_name))) &
        (Book.author_name.ilike('%{}%'.format(author_name))) &
        (Book.genre.ilike('%{}%'.format(genre))) &
        (Book.ISBN.ilike('%{}%'.format(ISBN)))
    )

    if publish_date:
        try:
            publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
        except Exception:
            abort(400, 'Bad request')
        books = books.filter_by(publish_date=publish_date)

    books = books_schema.dump(books).data
    if len(books) <= 0:
        abort(404, 'Book not found')

    return books, 200


def create():
    json_data = request.get_json(force=True)
    if not json_data:
        abort(400, "Bad Request for Create")

    data, errors = book_schema.load(json_data)
    if errors:
        abort(400, errors)
    book = Book.query.filter_by(ISBN=data.ISBN).first()

    if book:
        abort(400, "Book already exists")

    if json_data.get("count") <= 0:
        abort(400, "Bad Request for Book Create")

    new_book = Book(
        book_name=data.book_name,
        author_name=data.author_name,
        genre=data.genre,
        ISBN=data.ISBN,
        count=data.count,
        publish_date=data.publish_date
    )

    db.session.add(new_book)
    db.session.commit()
    result = book_schema.dump(new_book).data
    return result, 201


def update():
    request_book = request.get_json(force=True)
    if not request_book:
        abort(400, "No Input Data")

    data, errors = book_schema.load(request_book)
    if errors:
        abort(400, "Bad Request")

    book = Book.query.filter_by(ISBN=request_book['ISBN']).first()
    if not book:
        abort(404, 'Book Not Found')

    book.ISBN = data.ISBN
    book.book_name = data.book_name if data.book_name != None else book.book_name
    book.author_name = data.author_name \
        if data.author_name != None else book.author_name
    book.genre = data.genre if data.genre != None else book.genre
    book.publish_date = data.publish_date \
        if data.publish_date != None else book.publish_date
    book.count = data.count if data.count != None else book.count
    book.reservation_count = data.reservation_count \
        if data.reservation_count != None else book.reservation_count
    db.session.commit()

    result = book_schema.dump(book).data
    return result, 200


def delete():
    json_data = request.get_json(force=True)
    if not json_data:
        abort(400, "No Data Provided")

    book = Book.query.filter_by(ISBN=json_data['ISBN']).first()

    if not book:
        abort(404, 'Book Not Found')

    result = book_schema.dump(book).data

    db.session.delete(book)
    db.session.commit()
    return result, 200


def reserve_book():
    json_data = request.get_json(force=True)
    if not json_data:
        abort(400, "Bad request")

    book = Book.query.filter_by(ISBN=json_data.get("ISBN")).first()

    if not book:
        abort(404, "Not found")

    total_count = book.reservation_count + json_data.get("reservation_count")
    if total_count > book.count or json_data.get("reservation_count") <= 0:
        abort(400, "There is no book for your request")

    new_reserve = Reservation(
        book_ISBN=json_data.get("ISBN"),
        reservation_id=str(uuid.uuid4())[:5],
        reservation_count=json_data.get("reservation_count"),
        is_barrowed=False
    )

    book.reservation_count += json_data.get("reservation_count")
    db.session.add(new_reserve)
    db.session.commit()

    result = reservation_schema.dump(new_reserve).data
    return result, 201


def borrow_book():
    json_data = request.get_json(force=True)
    if not json_data:
        abort(400, 'Bad request')

    reservation = Reservation.query.filter_by(\
                    reservation_id=json_data.get('reservation_id')).first()
    if not reservation:
        abort(404, 'Reservation not found')

    book_isbn = reservation.book_ISBN
    book = Book.query.filter_by(ISBN=book_isbn).first()

    if reservation.is_barrowed == False:
        book.count -= reservation.reservation_count
        book.reservation_count -= reservation.reservation_count
        reservation.is_barrowed = True
        db.session.commit()
        result = book_schema.dump(book).data
        return result, 200
    else:
        abort(400, 'Bad request')


def return_book():
    json_data = request.get_json(force=True)
    if not json_data:
        abort(400, "Bad request")
    
    reservation_id = json_data.get("reservation_id")
    reservation = Reservation.query.filter_by(
                                    reservation_id=reservation_id).first()
    if not reservation:
        abort(404, "Reservation Not Found")
    book_isbn = reservation.book_ISBN
    book = Book.query.filter_by(ISBN=book_isbn).first()

    if reservation.is_barrowed:
        book.count += reservation.reservation_count
    else:
        abort(400, "Borrow is not completed, you can not return books")
    db.session.delete(reservation)
    db.session.commit()

    result = book_schema.dump(book).data
    return result, 200
