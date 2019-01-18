import connexion
import os
import json
from models import db, Book

username = "postgres"
password = ""
host = "localhost"
database = "flaskdb"

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db.init_app(app)

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
            db.session.commit()
        except:
            pass

with app.app_context():
    init_db_values()