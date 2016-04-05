# -*- coding: utf-8 -*-
"""
    yabab
    ~~~~~

    A backend bankding API for the fictional YaBaB Savings Bank.

    :copyright: (c) 2016 Alexis Hildebrandt
    :license: MIT, see LICENSE for more details.
"""

__author__  = "Alexis Hildebrandt"
__version__ = "0.0.1"
__license__ = "MIT"
__copyright__ = "Copyright 2016, Alexis Hildebrandt"

from flask import Flask, jsonify, current_app
from flask.json import JSONEncoder
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('app_conf')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_JSON()
        except AttributeError:
            JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


db = SQLAlchemy(app)

from . import blueprints
