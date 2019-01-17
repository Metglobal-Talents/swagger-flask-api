from models import Reservation, Book, db, BookSchema, ReservationSchema
from flask import request, abort
import uuid

books_schema = BookSchema(many=True)
book_schema = BookSchema()
reservations_schema = ReservationSchema(many=True)
reservation_schema = ReservationSchema()


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
        abort(404, 'Reservation not found')


def return_book():
    pass

