"""Portfolio - CONTROLLER

"""

from flask import Blueprint, render_template, request, redirect

from app import app
from app.helpers.decorators import requires_auth
from app.models.company import Company
from app.models.portfolio import Portfolio, PortfolioEvent

portfolio = Blueprint('Portfolio', __name__, url_prefix='/portfolio')


@portfolio.route('')
@requires_auth
def index():
    """
    Portfolio Index page

    """
    user_portfolio = Portfolio.query.filter(Portfolio.id == 1).one()

    # Get all the distinct companies out of the events
    company_ids = []
    positions = {}
    totals = {
        'profit': 0,
    }
    companies = {}

    for e in user_portfolio.events:

        if e.company_id not in companies:
            companies[e.company_id] = Company(e.company_id)

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
        print positions
        print ''
        print ''
        if 'num_shares' in position and position['num_shares'] == 0:
            totals['profit'] += positions[c_id]['profit']

    # company_qry = ''
    # for x in company_ids:
    #     company_qry += '%s,' % x
    # company_qry = company_qry[:-1]

    app.logger.info(company_ids)

    d = {
        'portfolio': user_portfolio,
        'companies': companies,
        'positions': positions,
        # 'company_qry': company_qry,
        'totals': totals
    }
    return render_template('portfolio/index.html', **d)


@portfolio.route('/event/form')
@portfolio.route('/event/form/<event_id>')
@requires_auth
def form_event(event_id=None):
    """
    Form for creating, saving and deleting a PortfolioEvent

    :param event_id: PortforlioEvent.id to be edited or deleted
    :type event_id: int
    """
    d = {}
    d['event'] = None
    d['edit'] = False
    if event_id:
        event = PortfolioEvent().query.filter(PortfolioEvent.id == event_id).one()
        if event:
            d['event'] = event
            d['edit'] = True
    return render_template('portfolio/event_form.html', **d)


@portfolio.route('/event/save', methods=['POST'])
@requires_auth
def save_event():
    """
    Save a new or update a PortfolioEvent

    """
    pe = PortfolioEvent()
    if request.form.get('id'):
        pe.id = request.form['id']
    pe.portfolio_id = request.form['portfolio_id']
    pe.company_id = request.form['company_id']
    pe.price = request.form['price']
    pe.type = request.form['type']
    pe.date = request.form['date']
    pe.count = request.form['count']
    pe.save()
    return redirect('/portfolio')


@portfolio.route('/event/delete/<event_id>')
@requires_auth
def delete_event(event_id):
    """
    Delete a PortfolioEvent, this needs to be locked down to users with access to this portfolio.

    :param event_id: PortforlioEvent.id to be deleted
    :type event_id: int
    """

    x = PortfolioEvent().query.filter(PortfolioEvent.id == event_id).one()
    return str(x)

# End File: stocky/app/controllers/portfolio.py
