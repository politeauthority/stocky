"""Company - Controller

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
        d['company'] = company
    except NoResultFound:
        return render_template('company/404.html'), 404
    d['quote_count'] = Quote.query.filter(Quote.company_id == company.id).count()

    # c_hit = CompanyMeta()
    # c_hit.key = 'web_hit'
    # c_hit.val_type = 'int'
    # c_hit.val_int =

    return render_template('company/info.html', **d)


# End File: stocky/app/controllers/company.py
