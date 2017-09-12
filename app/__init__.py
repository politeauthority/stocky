"""App

"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
if os.environ.get('STOCKY_BULD') == 'LIVE':
    app.config.from_pyfile('config/live.py')
else:
    app.config.from_pyfile('config/dev.py')
db = SQLAlchemy(app)

# Helpers
from app.helpers import misc_time
from app.helpers import common
from app.helpers import jinja_filters

# Controllers
from controllers.home import home as ctrl_home
from controllers.company import company as ctrl_company
from controllers.portfolio import portfolio as ctrl_portfolio


def register_logging(app):
    log_dir = os.path.join(app.config['APP_DATA_PATH'], 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    app_log_file = os.path.join(log_dir, 'stocky.log')
    logging.basicConfig(filename=app_log_file, level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = TimedRotatingFileHandler(
        app_log_file,
        when='midnight',
        backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def register_jinja_funcs(app):
    app.jinja_env.filters['time_ago'] = misc_time.ago
    app.jinja_env.filters['fmt_date'] = misc_time.fmt_date
    app.jinja_env.filters['fmt_currency'] = jinja_filters.format_currency
    app.jinja_env.filters['percentage'] = common.get_percentage


def register_blueprints(app):
    app.register_blueprint(ctrl_home)
    app.register_blueprint(ctrl_company)
    app.register_blueprint(ctrl_portfolio)

DebugToolbarExtension(app)
register_logging(app)
register_jinja_funcs(app)
register_blueprints(app)

app.logger.info('Started App!')
