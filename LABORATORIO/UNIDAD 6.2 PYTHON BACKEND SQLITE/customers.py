from flask import abort, make_response
from config import db
from models import Customer, customer_schema, customers_schema


def read_all():
    customers = Customer.query.all()
    return customers_schema.dump(customers)


def create(customer):
    lname = customer.get("lname")
    email = customer.get("email")

    existing_customer = Customer.query.filter(
        (Customer.lname == lname) | (Customer.email == email)
    ).one_or_none()

    if existing_customer is None:
        new_customer = customer_schema.load(customer, session=db.session)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer), 201
    else:
        abort(
            406,
            f"El cliente con apellido {lname} o email {email} ya existe"
        )


def read_one(lname):
    customer = Customer.query.filter(Customer.lname == lname).one_or_none()

    if customer is not None:
        return customer_schema.dump(customer)
    else:
        abort(404, f"Cliente con apellido {lname} no encontrado")


def update(lname, customer):
    existing_customer = Customer.query.filter(Customer.lname == lname).one_or_none()

    if existing_customer:
        update_customer = customer_schema.load(customer, session=db.session)
        existing_customer.fname = update_customer.fname
        existing_customer.email = update_customer.email
        existing_customer.phone = update_customer.phone
        db.session.merge(existing_customer)
        db.session.commit()
        return customer_schema.dump(existing_customer), 200
    else:
        abort(404, f"Cliente con apellido {lname} no encontrado")


def delete(lname):
    existing_customer = Customer.query.filter(Customer.lname == lname).one_or_none()

    if existing_customer:
        db.session.delete(existing_customer)
        db.session.commit()
        return make_response(f"Cliente {lname} eliminado con éxito", 200)
    else:
        abort(404, f"Cliente con apellido {lname} no encontrado")