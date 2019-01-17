from flask import make_response, abort, request


class Book:
    def __init__(self, book):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def to_json(self, args=None):
        pass

    def give_attribute_names(self):
        pass

    def __eq__(self, other):
        pass


class Library:

    def __init__(self):
        pass

    def read_json(self):
        pass


def reserve_book(ISBN):
    pass


def create_reservation(book, reservation_count):
    pass


def borrow_book(reservation_id):
    pass

def return_book(reservation_id):
    pass


library = Library()
