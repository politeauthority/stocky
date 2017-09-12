"""Home - Controller
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template
from sqlalchemy.orm.exc import NoResultFound
from app.models.company import Company
from app.models.quote import Quote

company = Blueprint('Company', __name__, url_prefix='/company')


@company.route('/<symbol>')
def index(symbol=None):
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
        return render_template('company/404.html')
    return render_template('company/info.html', **d), 404


# End File: stocky/app/controllers/company.py
