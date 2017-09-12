"""Company Collections

"""
import sys
sys.path.append("../..")
from app import app
from app.models.company import Company

watchlist_symbols = ['AAPLE', 'TSLA', 'ERIC', 'BAC', 'VWO', 'MSFT', 'AMD', 'VSLR', 'EFX', 'SPYD', 'TSLA', 'NFLX', 'FB',
                     'DIS', 'GPRO', 'SBUX', 'F', 'BABA', 'FIT', 'ABBS', 'INTC', 'TWTR', 'ERIC', 'VMW', 'T', 'EXF']


def by_symbols(symbols):
    """
    Get companies by symbol
    :param symbols:
    :type symbols: list
    :return: Company objects
    :rtype: SqlAlchemey result of company objects.
    """
    print symbols
    companies = Company.query.filter(Company.symbol.in_(symbols)).all()
    return companies


def watchlist():
    """
    Gets the watchlist Company objects all loaded up.

    :return: Company objects
    :rtype: SqlAlchemey result of company objects
    """
    return by_symbols(watchlist_symbols)

# End File: stocky/app/collections/companies.py