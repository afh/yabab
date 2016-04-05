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

from flask import Flask
app = Flask(__name__)
app.config.from_object('app_conf')

from . import blueprints
