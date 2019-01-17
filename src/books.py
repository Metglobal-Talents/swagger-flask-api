from flask import request
from models import Book, BookSchema

books_schema = BookSchema(many=True)


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
    pass


def update():
    pass


def delete():
    pass
