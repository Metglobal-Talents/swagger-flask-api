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

    if len(books) <= 0:
        abort(404, 'Book not found')

    books = books_schema.dump(books).data
    return books, 200


def create():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400, "Bad Request for Create")

        data, errors = book_schema.load(json_data)
        if errors:
            abort(400, errors)
        check = Book.query.filter_by(ISBN=data.ISBN).first()

        if check:
            abort(400, "Book already exists")

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
    pass


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
