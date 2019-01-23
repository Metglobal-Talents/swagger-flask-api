from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=False)
    author_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    ISBN = db.Column(db.String(13), unique=True, nullable=False)
    count = db.Column(db.Integer)
    reservation_count = db.Column(db.Integer, default=0)
    publish_date = db.Column(db.Date)


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    book_ISBN = db.Column(db.String(13))
    reservation_id = db.Column(db.String(5))
    reservation_count = db.Column(db.Integer)
    is_barrowed = db.Column(db.Boolean)


class BaseSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session


class BookSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Book


class ReservationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Reservation

class BookLoadSchema(ma.Schema):
    ISBN = fields.String(required=True)
    book_name = fields.String()
    author_name = fields.String()
    genre = fields.String()
    count = fields.Integer()
    reservation_count = fields.Integer()
    publish_date = fields.Date()




