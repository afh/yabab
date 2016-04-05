# -*- coding: utf-8 -*-
import json
from flask import Blueprint, Response, jsonify, request, current_app

from . import db, __version__
from .models import Customer, Account, Transaction
from .api_utils import *

mod = Blueprint('api', __name__)


@mod.route('/')
def root():
    result = db.session.query(Customer).first()
    current_app.logger.debug(result.name)
    response = {__name__: "v{}".format(__version__)}
    return jsonify(response)


@mod.route('/accounts',
           methods=['POST', 'GET'],
           defaults={'account_number': None})
@mod.route('/accounts/<account_number>', methods=['GET'])
def accounts(account_number):
    """Routes requests to `create_account()` or `show_balance()`"""
    if request.method == 'POST':
        return create_account(get_data(request))
    elif request.method == 'GET' and account_number:
        return show_balance(account_number)
    else:
        return error("Error processing {} request for account number {}".format(request.method, account_number))

def create_account(data):
    """Creates a new account for a customer identified by customer_id"""
    mandatory_params = ['customer_id', 'initial_deposit']
    result = check_required_params(mandatory_params, data)
    if result:
        return result

    customer = Customer.query.filter_by(id=data['customer_id']).first()
    if not customer:
        return error("No customer with id {} found".format(data['customer_id']), 404)

    new_account = Account(customer.id)
    db.session.add(new_account)
    db.session.commit()

    (amount, error) = validate_amount('initial_deposit', data)
    if error:
        return error

    ## NOTE: It seems odd to have the new_account.id as both the originator and the beneficiary here
    new_transaction = Transaction(new_account.id, new_account.id, 'Initial Deposit', amount)
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"account_number": new_account.number}), 201

def show_balance(account_number):
    return jsonify({"balance": "Balance for {}".format(account_number)})


@mod.route('/transactions', methods=['POST'])
def create_transaction():
    data = get_data(request)
    mandatory_params = ['amount', 'reference', 'originator', 'beneficiary']
    result = check_required_params(mandatory_params, data)
    if result:
        return result

    (originator, error) = get_account('originator', data)
    if error:
        return error

    (beneficiary, error) = get_account('beneficiary', data)
    if error:
        return error

    (amount, error) = validate_amount('amount', data)
    if error:
        return error

    originator_transaction = Transaction(originator.id, beneficiary.id, data['reference'], -amount)
    beneficiary_transaction = Transaction(beneficiary.id, originator.id, data['reference'], amount)
    db.session.add(originator_transaction)
    db.session.add(beneficiary_transaction)
    db.session.commit()

    return jsonify({"transaction": originator_transaction.id}), 201


@mod.route('/accounts/<account_number>/transactions', methods=['GET'])
def account_transactions(account_number):
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        return error("No account with number {} found".format(account_number), 404)
    transactions = Transaction.query.filter_by(originator=account.id).order_by('datetime').all()
    return jsonify({"account_number": account.number, "transactions": transactions})
