"""Home - CONTROLLER
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template
from sqlalchemy.orm.exc import NoResultFound
from app.models.company import Company
from app.models.quote import Quote

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    return render_template('home/index.html')


@home.route('dashboard')
def dashboard():
    d = {}
    d['data_stats'] = {
        'total_companies': Company.query.count(),
        'total_quotes': Quote.query.count(),
        'recent_companies': Company.query.filter().order_by(Company.ts_updated.desc()).limit(10)
    }
    return render_template('home/dashboard.html', **d)


@home.route('company/<symbol>')
def company(symbol=None):
    """
    Company Info page

    :param symbol: stock symbol
    :type symbol: str
    """
    d = {}
    try:
        company = Company.query.filter(Company.symbol == symbol).one()
        quotes = Quote.query.filter(Quote.company_id == company.id).all()
        d['company'] = company
        d['quotes'] = quotes
    except NoResultFound:
        return render_template('home/company_404.html')
    return render_template('home/company.html', **d), 404


@home.route('companies')
def companies():
    c_query = Company.query.order_by(Company.ts_updated)
    d = {}
    d['companies'] = Company.query.order_by(Company.ts_updated).all()
    d['total_companies'] = c_query.count()
    return render_template('home/companies.html', **d)

# End File: app/controllers/home.py
