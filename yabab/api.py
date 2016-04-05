# -*- coding: utf-8 -*-
import json
from flask import Blueprint, current_app

from . import db, __version__
from .models import Customer, Account, Transaction

mod = Blueprint('api', __name__)

@mod.route('/')
def root():
    result = db.session.query(Customer).first()
    current_app.logger.debug(result.name)
    response = {__name__: "v{}".format(__version__)}
    return json.dumps(response)
