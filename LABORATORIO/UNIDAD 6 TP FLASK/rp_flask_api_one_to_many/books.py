from flask import abort, make_response
from config import db
from models import Author, Book, book_schema

def read_one(book_id):
    book = Book.query.get(book_id)
    if book is not None:
        return book_schema.dump(book)
    else:
        abort(404, f"Libro con ID {book_id} no encontrado")

def update(book_id, book):
    existing_book = Book.query.get(book_id)
    if existing_book:
        update_book = book_schema.load(book, session=db.session)
        existing_book.title = update_book.title
        db.session.merge(existing_book)
        db.session.commit()
        return book_schema.dump(existing_book), 201
    else:
        abort(404, f"Libro con ID {book_id} no encontrado")

def delete(book_id):
    existing_book = Book.query.get(book_id)
    if existing_book:
        db.session.delete(existing_book)
        db.session.commit()
        return make_response(f"Libro {book_id} eliminado con éxito", 200)
    else:
        abort(404, f"Libro con ID {book_id} no encontrado")

def create(book):
    author_id = book.get("author_id")
    author = Author.query.get(author_id)
    if author:
        new_book = book_schema.load(book, session=db.session)
        author.books.append(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201
    else:
        abort(404, f"Autor no encontrado con ID: {author_id}")