"""App
Main file for the entire flask app.

"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import flask_restless

app = Flask(__name__)
if os.environ.get('STOCKY_BUILD') == 'LIVE':
    app.config.from_pyfile('config/live.py')
else:
    app.config.from_pyfile('config/dev.py')
db = SQLAlchemy(app)

from app.models.company import Company
from app.models.quote import Quote

# Helpers
from app.helpers import misc_time
from app.helpers import common
from app.helpers import jinja_filters

# Controllers
from controllers.home import home as ctrl_home
from controllers.company import company as ctrl_company
from controllers.portfolio import portfolio as ctrl_portfolio
from controllers.search import search as ctrl_search


def register_logging(app):
    """
    Connects the logging to the app.

    """
    log_dir = os.path.join(app.config['APP_DATA_PATH'], 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    app_log_file = os.path.join(log_dir, 'stocky.log')
    handler = TimedRotatingFileHandler(app_log_file, when='midnight', interval=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


def register_jinja_funcs(app):
    """
    Makes functions avialble to jinja templates.

    """
    app.jinja_env.filters['time_ago'] = misc_time.ago
    app.jinja_env.filters['fmt_date'] = misc_time.fmt_date
    app.jinja_env.filters['fmt_currency'] = jinja_filters.format_currency
    app.jinja_env.filters['percentage'] = common.get_percentage


def register_blueprints(app):
    """
    Connect the blueprints to the router.

    """
    app.register_blueprint(ctrl_home)
    app.register_blueprint(ctrl_company)
    app.register_blueprint(ctrl_portfolio)
    app.register_blueprint(ctrl_search)


def register_api(app):
    """
    Enables the API routes and configruation.

    """
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(Company, methods=['GET'])
    manager.create_api(Quote, methods=['GET'], max_results_per_page=365)

DebugToolbarExtension(app)
register_logging(app)
register_jinja_funcs(app)
register_blueprints(app)
register_api(app)

app.logger.info('Started App!')
