"""Search - Controller

"""
from flask import Blueprint, render_template, request

from app.models.company import Company

search = Blueprint('Search', __name__, url_prefix='/search')


@search.route('')
def index():
    """
    Search Home

    :param symbol: stock symbol
    :type symbol: str
    """
    industry_seach = False
    if request.args.get('industry'):
        industry_seach = request.args.get('industry')

    query_filters = []
    if industry_seach:
        query_filters.append(Company.industry == industry_seach)

    search_results = Company.query.filter(Company.industry == industry_seach).all()
    d = {
        'search_results': search_results
    }
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
