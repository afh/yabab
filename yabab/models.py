import random

from . import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(), unique=True)
    customer = db.Column(db.Integer, db.ForeignKey('{}.id'.format(Customer.__tablename__)))

    def __init__(self, customer):
        self.number = self.new_account_number()
        self.customer = customer

    # TODO: Find a possibility to ensure account_number uniqueness
    #       without querying the database
    def new_account_number(self):
        while True:
            new_account_number = Account.generate_account_number()
            account = Account.query.filter_by(number=new_account_number).first()
            if not account:
                return new_account_number

    @classmethod
    def generate_account_number(cls):
        return '{:0>10}'.format(random.randint(1000000, 999999999))

    def to_JSON(self):
        customer = Customer.query.get(self.customer)
        return {"id": self.id,
                "number": self.number,
                "customer": customer.name,
                "customer_id": customer.id,
               }


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=db.func.now())
    originator = db.Column(db.Integer, db.ForeignKey('{}.id'.format(Account.__tablename__)))
    beneficiary = db.Column(db.Integer, db.ForeignKey('{}.id'.format(Account.__tablename__)))
    reference = db.Column(db.String())
    amount = db.Column(db.Numeric)

    def __init__(self, originator, beneficiary, reference, amount):
        self.originator = originator
        self.beneficiary = beneficiary
        self.reference = reference
        self.amount = amount

    def to_JSON(self):
        originator = Account.query.get(self.originator)
        beneficiary = Account.query.get(self.beneficiary)
        return {"id": self.id,
                "date": self.datetime.strftime('%Y-%m-%d'),
                "originator": originator.number,
                "beneficiary": beneficiary.number,
                "amount": float(self.amount)
               }
