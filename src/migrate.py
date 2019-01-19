from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Book
from config import app
import os
import json


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def dropdb():
    db.drop_all()

@manager.command
def initial_values():
    init_db_values()

def read_json_file():
    books_path = os.path.join(os.path.dirname(__file__), 'books.json')
    with open(books_path, "r") as f:
        data = f.read()
    return data

def init_db_values():
    books = json.loads(read_json_file())
    for book in books:
        new_book = Book(
            ISBN=book.get("ISBN"),
            book_name=book.get("book_name"),
            author_name=book.get("author_name"),
            genre=book.get("genre"),
            publish_date=book.get("publish_date"),
            count=int(book.get("count")),
            reservation_count=int(book.get("reservation_count"))
        )
        try:
            db.session.add(new_book)
        except:
            pass
    db.session.commit()


if __name__ == '__main__':
    manager.run()
