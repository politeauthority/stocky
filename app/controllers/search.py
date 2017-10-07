"""Search - Controller

"""
from flask import Blueprint, render_template, request, redirect

from app.models.company import Company

search = Blueprint('Search', __name__, url_prefix='/search')


@search.route('', methods=['GET', 'POST'])
def index():
    """
    Search Home

    :param symbol: stock symbol
    :type symbol: str
    """
    search_phrase = None
    if 'search' in request.form:
        search_phrase = request.form['search']
    industry_phrase = None
    if 'industry' in request.args:
        industry_phrase = request.args['industry']
    # return str()
    companies_seach = []
    if search:
        companies_seach = Company.query.filter(Company.symbol.like("%" + search_phrase + "%"))\
            .order_by(Company.ts_updated).all()
        companies_seach += Company.query.filter(Company.name.like("%" + search_phrase + "%"))\
            .order_by(Company.ts_updated).all()
    if industry_phrase:
        companies_seach += Company.query.filter(Company.industry.like("%" + industry_phrase + "%"))\
            .order_by(Company.ts_updated).all()
    if len(companies_seach) == 1:
        return redirect('/company/%s' % companies_seach[0].symbol)
    d = {
        'companies': companies_seach,
        'search_term': request.form['search']
    }
    # companies_seach = Company.query.filter(Company.symbol == request.form['search']).all()
    return render_template('search/results.html', **d)


@search.route('companies')
def companies():
    """
    Search companies

    """
    d = {}
    return str(request.form["sector"])
    return render_template('search/companies.html', **d)

# End File: stocky/app/controllers/search.py
