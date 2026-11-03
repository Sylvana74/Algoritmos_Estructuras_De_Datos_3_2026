from flask import abort, make_response
from config import db
from models import Author, author_schema, authors_schema

def read_all():
    authors = Author.query.all()
    return authors_schema.dump(authors)

def read_one(lname):
    author = Author.query.filter(Author.lname == lname).one_or_none()
    if author is not None:
        return author_schema.dump(author)
    else:
        abort(404, f"Autor con apellido {lname} no encontrado")

def create(author):
    lname = author.get("lname")
    existing_author = Author.query.filter(Author.lname == lname).one_or_none()
    if existing_author is None:
        new_author = author_schema.load(author, session=db.session)
        db.session.add(new_author)
        db.session.commit()
        return author_schema.dump(new_author), 201
    else:
        abort(406, f"El autor con apellido {lname} ya existe")

def update(lname, author):
    existing_author = Author.query.filter(Author.lname == lname).one_or_none()
    if existing_author:
        update_author = author_schema.load(author, session=db.session)
        existing_author.fname = update_author.fname
        db.session.merge(existing_author)
        db.session.commit()
        return author_schema.dump(existing_author), 201
    else:
        abort(404, f"Autor con apellido {lname} no encontrado")

def delete(lname):
    existing_author = Author.query.filter(Author.lname == lname).one_or_none()
    if existing_author:
        db.session.delete(existing_author)
        db.session.commit()
        return make_response(f"{lname} eliminado con éxito", 200)
    else:
        abort(404, f"Autor con apellido {lname} no encontrado")