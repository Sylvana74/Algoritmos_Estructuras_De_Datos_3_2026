from datetime import datetime
from config import db, ma


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True, nullable=False)
    fname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(32), nullable=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)