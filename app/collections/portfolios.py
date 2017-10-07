"""Portfolio - COLLECTION

"""
import sys
sys.path.append("../..")

from app.models.company import Company
from app.models.portfolio import Portfolio


def by_portfolio(portfolio_id):
    """
    Get portfolio calculations by portfolio_id

    :param portfolio_id:
    :type portfolio_id: int
    :return:
    :rtype: dict
    """
    user_portfolio = Portfolio.query.filter(Portfolio.id == portfolio_id).one()

    positions = {}
    totals = {
        'profit': 0,
    }
    companies = {}

    for e in user_portfolio.events:
        local_companh_id = e.company_id
        # if e.company_id not in companies:
            # companies[local_companh_id] = Company(local_companh_id)

        if e.company_id not in positions:
            positions[e.company_id] = {}
            positions[e.company_id]['investment'] = 0
            positions[e.company_id]['num_shares'] = 0
            positions[e.company_id]['profit'] = 0

        if e.type == 'sell':
            # positions[e.company_id]['investment'] += (e.price * e.count)
            positions[e.company_id]['profit'] += (e.price * e.count)
            positions[e.company_id]['num_shares'] += e.count

        elif e.type == 'dividend':
            positions[e.company_id]['profit'] += (e.price * e.count)

        elif e.type == 'buy':
            positions[e.company_id]['investment'] += (e.price * e.count)
            positions[e.company_id]['profit'] = positions[e.company_id]['profit'] - (e.price * e.count)
            positions[e.company_id]['num_shares'] = positions[e.company_id]['num_shares'] - e.count

    for c_id, position in positions.iteritems():
        if 'num_shares' in position and position['num_shares'] == 0:
            totals['profit'] += positions[c_id]['profit']

    return {
        'positions': positions,
        'companies': companies,
        'totals': totals,
        'portfolio': user_portfolio
    }


def by_user_id(user_id):
    """
    Get all portfolios by the users id.

    :param user_id: The users id
    :type user_id: int
    :return: List SQL Alchemey Portfolio objects.
    :rtype: list
    """
    return Portfolio.query.filter(Portfolio.user_id == user_id).all()

# End File: stocky/app/collections/portfolios.py
