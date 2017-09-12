"""Home - Controller
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template

from app.collections import companies as cc
from app.models.company import Company
from app.models.quote import Quote

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    """
    Index
    Nothing really here yet.

    """
    return render_template('home/index.html')


@home.route('dashboard')
def dashboard():
    """
    Dashboard
    Displays some statictics about the site, we'll probably hide these eventually

    """
    d = {}
    d['data_stats'] = {
        'total_companies': Company.query.count(),
        'total_quotes': Quote.query.count(),
        'recent_companies': Company.query.filter().order_by(Company.ts_updated.desc()).limit(10)
    }
    return render_template('home/dashboard.html', **d)


@home.route('companies')
def companies():
    """
    Companies Roster Page
    @todo this should be paginated

    """
    c_query = Company.query.order_by(Company.ts_updated)
    d = {}
    d['companies'] = Company.query.order_by(Company.ts_updated).all()
    d['total_companies'] = c_query.count()
    return render_template('home/companies.html', **d)


@home.route('watchlist')
def watchlist():
    """
    Companies from the watch list

    """
    # c_query = Company.query.order_by(Company.ts_updated)
    d = {}
    d['companies'] = cc.watchlist()
    return render_template('home/watchlist.html', **d)

# End File: stocky/app/controllers/home.py
