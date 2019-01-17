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


def reserve_book():
    pass

def borrow_book():
    pass

def return_book():
    pass


library = Library()
