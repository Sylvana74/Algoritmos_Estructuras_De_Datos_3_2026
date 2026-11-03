from datetime import datetime
from config import app, db
from models import Author, Book

AUTHORS_BOOKS = [
    {
        "fname": "Gabriel",
        "lname": "García Márquez",
        "books": [
            ("Cien años de soledad", "2023-01-06 17:10:24"),
            ("El amor en los tiempos del cólera", "2023-03-05 22:17:54"),
            ("Crónica de una muerte anunciada", "2023-03-05 22:18:10"),
        ],
    },
    {
        "fname": "Jorge Luis",
        "lname": "Borges",
        "books": [
            ("Ficciones", "2023-01-01 09:15:03"),
            ("El Aleph", "2023-02-06 13:09:21"),
        ],
    },
    {
        "fname": "Julio",
        "lname": "Cortázar",
        "books": [
            ("Rayuela", "2023-01-07 22:47:54"),
            ("Bestiario", "2023-04-06 13:03:17"),
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for data in AUTHORS_BOOKS:
        author = Author(lname=data.get("lname"), fname=data.get("fname"))
        for title, timestamp in data.get("books", []):
            author.books.append(
                Book(
                    title=title,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )
        db.session.add(author)

    db.session.commit()
    print("Base de datos library.db creada con éxito.")