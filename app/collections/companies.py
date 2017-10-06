"""Company Collections

"""
import sys
sys.path.append("../..")

from app.models.company import Company

watchlist_symbols = ['AAPL', 'TSLA', 'ERIC', 'BAC', 'VWO', 'MSFT', 'AMD', 'VSLR', 'EFX', 'SPYD', 'TSLA', 'NFLX', 'FB',
                     'DIS', 'GPRO', 'SBUX', 'F', 'BABA', 'FIT', 'ABBS', 'INTC', 'TWTR', 'ERIC', 'VMW', 'T', 'EXF',
                     'ORCL', 'RDFN', 'CACQ']


def by_symbols(symbols):
    """
    Get companies by symbol

    :param symbols:
    :type symbols: list
    :return: Company objects
    :rtype: list SqlAlchemey result of company objects.
    """
    companies = Company.query.filter(Company.symbol.in_(symbols)).all()
    return companies


def by_symbols_as_dict(symbols):
    """
    Get companies by symbol returned as a dict keyed by company id

    :param symbols:
    :type symbols: list
    :return: Company objects
    :rtype: dict SqlAlchemey result of company objects.
    """
    companies = Company.query.filter(Company.symbol.in_(symbols)).all()
    ret_companies = {}
    for c in companies:
        ret_companies[c.id] = c
    return ret_companies


def watchlist():
    """
    Gets the watchlist Company objects all loaded up.

    :return: Company objects
    :rtype: SqlAlchemey result of company objects
    """
    return by_symbols(watchlist_symbols)


def all(order_by=None):
    """
    Gets all companies in the database

    :return: Company objects
    :rtype: SqlAlchemey result of company objects
    """
    return Company.query.all()

# End File: stocky/app/collections/companies.py
