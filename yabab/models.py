from . import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    customer = db.Column(db.Integer, db.ForeignKey('{}.id'.format(Customer.__tablename__)))


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    originator = db.Column(db.Integer, db.ForeignKey('{}.id'.format(Account.__tablename__)))
    beneficiary = db.Column(db.Integer, db.ForeignKey('{}.id'.format(Account.__tablename__)))
    reference = db.Column(db.String())
    amount = db.Column(db.Numeric)
