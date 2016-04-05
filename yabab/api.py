# -*- coding: utf-8 -*-
import json
from flask import Blueprint, current_app

from . import __version__

mod = Blueprint('api', __name__)

@mod.route('/')
def root():
    response = {__name__: "v{}".format(__version__)}
    return json.dumps(response)
