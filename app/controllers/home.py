"""Home - Controller
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template

from app.collections import companies as cc
from app.models.company import Company, CompanyDividend
from app.models.quote import Quote
from app.helpers import common

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


@home.route('dividends')
def dividends():
    """
    Get upcomming and recently passed dividends

    """
    # prelimiary_filter = CompanyDividend.eff_date >= (datetime.now() - timedelta(days=5))
    dividends = CompanyDividend.query.order_by(CompanyDividend.eff_date.desc()).limit(50).all()
    companies = {}
    for divy in dividends:
        if divy.company_id not in companies:
            companies[divy.company_id] = Company.query.filter(Company.id == divy.company_id).one()
    d = {}
    d['companies'] = companies
    d['dividends'] = dividends
    return render_template('home/dividends.html', **d)


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
    d = {
        'database_file_size': common.get_db_zip_size()
    }
    return render_template('home/about.html', **d)


@home.route('data-structure')
def data_structure():
    """
    Static data structure page.

    """
    return render_template('home/data_structure.html')


@home.route('tos')
def tos():
    """
    Terms of Service, static page.

    """
    return render_template('home/tos.html')

# End File: stocky/app/controllers/home.py
