#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from yabab import app, db

app.config.from_object('app_conf')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
