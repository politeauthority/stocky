"""Company - Controller

"""
from datetime import datetime, timedelta
from sqlalchemy import desc

from flask import Blueprint, render_template
from sqlalchemy.orm.exc import NoResultFound

from app.models.company import Company, CompanyMeta
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
        d['company'] = company
    except NoResultFound:
        return render_template('company/404.html')

    quote_filter_args = Quote.company_id == company.id and Quote.date >= datetime.now() - timedelta(days=365)
    quotes = Quote.query.filter(quote_filter_args).all()
    d['quotes'] = quotes

    # This should be moved to something that gets calculated when we get new queries.
    d['low_52_week'] = Quote.query.filter(quote_filter_args).order_by(Quote.low).limit(1).one().low
    d['high_52_week'] = Quote.query.filter(quote_filter_args).order_by(desc(Quote.high)).limit(1).one().high

    # c_hit = CompanyMeta()
    # c_hit.key = 'web_hit'
    # c_hit.val_type = 'int'
    # c_hit.val_int =

    return render_template('company/info.html', **d), 404


# End File: stocky/app/controllers/company.py
