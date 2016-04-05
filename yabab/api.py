# -*- coding: utf-8 -*-
import json
from flask import Blueprint, Response, jsonify, request, current_app

from . import db, __version__
from .models import Customer, Account, Transaction
from .api_utils import *

mod = Blueprint('api', __name__)

###########################################################################
# api_info
###########################################################################
@mod.route('/')
def api_info():
    response = {'message': 'Welcome to the YaBaB API',
                'version': 'v{}'.format(__version__)}
    return jsonify(response)


###########################################################################
# /accounts
###########################################################################
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
        return list_accounts()

def list_accounts():
    accounts = Account.query.all()
    return jsonify({"accounts": accounts})

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

    (amount, reject) = numeric_amount('initial_deposit', data)
    if reject:
        return reject

    ## NOTE: It seems odd to have the new_account.id as both the originator and the beneficiary here
    new_transaction = Transaction(new_account.id, new_account.id, 'Initial Deposit', amount)
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"account_number": new_account.number}), 201

def show_balance(account_number):
    """Show the current balance of an account identified by account_number"""
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        return error("No account with number {} found".format(account_number), 404)

    transactions = Transaction.query.filter_by(originator=account.id).order_by('datetime').all()
    balance = float(sum([t.amount for t in transactions]))
    return jsonify({"balance": balance})

@mod.route('/accounts/<account_number>/transactions', methods=['GET'])
def account_transactions(account_number):
    """List transactions for account identified by account_number"""
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        return error("No account with number {} found".format(account_number), 404)
    transactions = Transaction.query.filter_by(originator=account.id).order_by('datetime').all()
    return jsonify({"account_number": account.number, "transactions": transactions})


###########################################################################
# /transactions
###########################################################################
@mod.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction.
    For every request to this API endpoint two Transaction database entries
    are made in order to have some sort of double entry bookkeeping.
    """
    data = get_data(request)
    mandatory_params = ['amount', 'reference', 'originator', 'beneficiary']
    result = check_required_params(mandatory_params, data)
    if result:
        return result

    (originator, reject) = get_account('originator', data)
    if reject:
        return reject

    (beneficiary, reject) = get_account('beneficiary', data)
    if reject:
        return reject

    (amount, reject) = numeric_amount('amount', data)
    if reject:
        return reject

    originator_transaction = Transaction(originator.id, beneficiary.id, data['reference'], -amount)
    beneficiary_transaction = Transaction(beneficiary.id, originator.id, data['reference'], amount)
    db.session.add(originator_transaction)
    db.session.add(beneficiary_transaction)
    db.session.commit()

    # NOTE: Would it be confusing if the identifiers of both created transactions would be returned?
    return jsonify({"transaction": originator_transaction.id}), 201

