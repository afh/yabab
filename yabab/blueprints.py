# -*- coding: utf-8 -*-
from . import app
from . import api

app.register_blueprint(api.mod, url_prefix='/api')
