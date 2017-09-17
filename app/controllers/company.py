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
    quotes = Quote.query.filter(Quote.company_id == company.id).all()
    d['quotes'] = quotes
    d['52_week_low'] = int(Quote.query.filter(
        Quote.company_id == 26 and
        Quote.date >= datetime.now() - timedelta(days=365)).order_by(desc(Quote.low)).limit(1).one().low)
    d['52_week_high'] = int(Quote.query.filter(
        Quote.company_id == 26 and
        Quote.date >= datetime.now() - timedelta(days=365)).order_by(Quote.high).limit(1).one().high)
    # return str(d['52_week_low'])
    c_hit = CompanyMeta()
    c_hit.key = 'web_hit'
    c_hit.val_type = 'int'
    return render_template('company/info.html', **d), 404


# End File: stocky/app/controllers/company.py
