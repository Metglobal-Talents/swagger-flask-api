from flask import request
from models import Book, BookSchema, db

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
    try:
        book_name = request.args['book_name']
        author_name = request.args['author_name']
        genre = request.args['genre']
        ISBN = request.args['ISBN']
        publish_date = request.args['publish_date']
        count = request.args['count']
        reservation_count = request.args['reservation_count']
    except KeyError:
        return {"status": "Bad Request", "message": "No input provided"}, 400

    book = Book.query.get(ISBN)

    if book:
        return {"status": "conflict", "message": "Book already exist"}, 409

    book = Book(
        book_name=book_name,
        author_name=author_name,
        genre=genre,
        ISBN=ISBN,
        publish_date=publish_date,
        count=count,
        reservation_count=reservation_count
    )
    db.session.add(book)
    db.session.commit(book)
    result = books_schema.load(book).data
    return {"status": "Success", "data": result}, 201


def update():
    pass


def delete():
    pass
