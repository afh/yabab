# -*- coding: utf-8 -*-
from flask import jsonify, request

from .models import Account

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

def check_required_params(params, data):
    for param in params:
        result = check_required_param(param, data)
        if result:
            return result

def check_required_param(param, data):
    """Check if `data` contains mandatory parameter `param`"""
    if not data:
        return error("Missing mandatory parameter {}".format(param))
    try:
        data[param]
    except KeyError:
        return error("Missing mandatory parameter {}".format(param))
    return None

def get_account(param, data):
    """Return account model if account referenced by number in data exists, error otherwise"""
    account = Account.query.filter_by(number=data[param]).first()
    if not account:
        return (None, error("Invalid {} account number {}".format(param, data[param])))
    return (account, None)

