from flask import request, abort
from models import Book, BookSchema, db


books_schema = BookSchema(many=True)
book_schema = BookSchema()

def search():
    if request.method == ['GET']:
        book_name = request.args.get('book_name', '')
        author_name = request.args.get('author_name', '')
        genre = request.args.get('genre', '')
        ISBN = request.args.get('ISBN', '')
        publish_date = request.args.get('publish_date', '')

        books = Book.query.filter(
            (Book.book_name.ilike('%{}%'.format(book_name))) |
            (Book.author_name.ilike('%{}%'.format(author_name))) |
            (Book.genre.ilike('%{}%'.format(genre))) |
            (Book.ISBN.ilike('%{}%'.format(ISBN))) |
            (Book.publish_date.ilike('%{}%'.format(publish_date)))
        )
        books = books_schema.dump(books).data
        return {books}, 200
    else:
        return 400


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
    pass