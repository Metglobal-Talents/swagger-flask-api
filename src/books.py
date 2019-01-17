from flask import request, abort
from models import Book, BookSchema, db
from datetime import datetime

books_schema = BookSchema(many=True)
book_schema = BookSchema()


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
        except TypeError:
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

    book.ISBN = request_book.get('ISBN')
    book.book_name = request_book.get('book_name', book.book_name)
    book.author_name = request_book.get('author_name', book.author_name)
    book.genre = request_book.get('genre', book.genre)
    book.publish_date = request_book.get('publish_date', book.publish_date)
    book.count = request_book.get('count', book.count)
    book.reservation_count = request_book.get('reservation_count',
                                              book.reservation_count)
    db.session.commit()

    result = book_schema.dump(book).data
    return result, 200


def delete():
    if request.method == 'DELETE':
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
