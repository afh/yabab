# -*- coding: utf-8 -*-
from flask import Blueprint, Response, jsonify, request, current_app

from . import db, __version__
from .models import Customer, Account, Transaction

mod = Blueprint('api', __name__)

def get_data(request):
    """Get data from request either from form-data or json body"""
    data = request.form
    if not data:
        data = request.get_json()
    return data

def error(message, status=200):
    """Wrap an error message in a response JSON"""
    data = {"status": "error", "reason": message}
    return jsonify(data), status

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
    try:
        customer_id = data['customer_id']
    except KeyError:
        return error("Missing mandatory parameter customer_id")

    customer = Customer.query.filter_by(id=customer_id).first()
    if not customer:
        return error("No customer with id {} found".format(customer_id), 404)

    new_account = Account(customer_id)
    db.session.add(new_account)
    db.session.commit()

    return jsonify({"account_number": new_account.number}), 201

def show_balance(account_number):
    return jsonify({"balance": "Balance for {}".format(account_number)})
