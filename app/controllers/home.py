"""Home - Controller
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template

from app.collections import companies as cc
from app.models.company import Company, CompanyDividend
from app.models.quote import Quote

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    """
    Index

    """
    d = {}
    d['data_stats'] = {
        'total_companies': Company.query.count(),
        'total_quotes': Quote.query.count(),
        'total_dividends': CompanyDividend.query.count(),
        'recent_companies': Company.query.filter().order_by(Company.ts_updated.desc()).limit(10).all()
    }
    return render_template('home/index.html', **d)


@home.route('dashboard')
def dashboard():
    """
    Dashboard
    Displays some statictics about the site, we'll probably hide these eventually

    @note: This methods basically just the index right now.

    """
    d = {}
    d['data_stats'] = {
        'total_companies': Company.query.count(),
        'total_quotes': Quote.query.count(),
        'total_dividends': CompanyDividend.query.count(),
        'recent_companies': Company.query.filter().order_by(Company.ts_updated.desc()).limit(10).all()
    }
    return render_template('home/dashboard.html', **d)


@home.route('recent')
def recently_updated():
    """
    Recently updated companies
    @todo: this should be paginated.

    """
    c_query = Company.query.order_by(Company.ts_updated)
    d = {}
    d['companies'] = Company.query.order_by(Company.ts_updated.desc()).limit(25).all()
    d['total_companies'] = c_query.count()
    return render_template('home/recent.html', **d)


@home.route('watchlist')
def watchlist():
    """
    Companies from the watch list

    """
    # c_query = Company.query.order_by(Company.ts_updated)
    d = {}
    d['companies'] = cc.watchlist()
    return render_template('home/watchlist.html', **d)


@home.route('about')
def about():
    """
    Static about page

    """
    return render_template('home/about.html')

@home.route('data-structure')
def data_structure():
    """
    Static data structure page.

    """
    return render_template('home/data_structure.html')

# End File: stocky/app/controllers/home.py
