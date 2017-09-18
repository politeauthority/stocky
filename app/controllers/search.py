"""Search - Controller

"""
from flask import Blueprint, render_template, request

search = Blueprint('Search', __name__, url_prefix='/search')


@search.route('')
def index():
    """
    Search Home

    :param symbol: stock symbol
    :type symbol: str
    """
    d = {}
    return render_template('search/index.html', **d)


@search.route('companies')
def companies():
    """
    Search companies

    """
    d = {}
    return str(request.form["sector"])
    return render_template('search/companies.html', **d)

# End File: stocky/app/controllers/search.py
