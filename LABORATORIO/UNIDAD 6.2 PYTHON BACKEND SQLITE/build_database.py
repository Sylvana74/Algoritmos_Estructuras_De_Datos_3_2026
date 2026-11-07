from datetime import datetime
from config import app, db
from models import Customer

CUSTOMERS = [
    {
        "fname": "Mariana",
        "lname": "Gomez",
        "email": "mariana.gomez@example.com",
        "phone": "+54 9 223 555-0101",
    },
    {
        "fname": "Lucas",
        "lname": "Perez",
        "email": "lucas.perez@example.com",
        "phone": "+54 9 223 555-0102",
    },
    {
        "fname": "Valeria",
        "lname": "Fernandez",
        "email": "valeria.f@example.com",
        "phone": "+54 9 223 555-0103",
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for customer_data in CUSTOMERS:
        new_customer = Customer(
            fname=customer_data["fname"],
            lname=customer_data["lname"],
            email=customer_data["email"],
            phone=customer_data["phone"],
            timestamp=datetime.utcnow(),
        )
        db.session.add(new_customer)
    db.session.commit()
    print("Base de datos customers.db creada y poblada con éxito.")