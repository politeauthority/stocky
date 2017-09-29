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
    for e in user_portfolio.events:
        if e.company_id not in company_ids:
            company_ids.append(e.company_id)
        if e.company_id not in positions:
            positions[e.company_id] = {}
            positions[e.company_id]['investment'] = 0
            positions[e.company_id]['num_shares'] = 0
        if e.type == 'buy':
            positions[e.company_id]['investment'] += (e.price * e.count)
            positions[e.company_id]['num_shares'] += e.count
        elif e.type == 'sell':
            positions[e.company_id]['investment'] = positions[e.company_id]['investment'] - e.price
            positions[e.company_id]['num_shares'] = positions[e.company_id]['num_shares'] - e.count

    company_qry = ''
    for x in company_ids:
        company_qry += '%s,' % x
    company_qry = company_qry[:-1]

    app.logger.info(company_ids)

    # Load the companeis
    companies = {}
    for c_id in company_ids:
        companies[c_id] = Company(c_id)

    d = {
        'portfolio': user_portfolio,
        'companies': companies,
        'positions': positions,
        'company_qry': company_qry
    }
    return render_template('portfolio/index.html', **d)


@portfolio.route('/event/form')
@requires_auth
def form_event():
    return render_template('portfolio/add_event.html')


@portfolio.route('/event/add', methods=['POST'])
@requires_auth
def add_event():
    pe = PortfolioEvent()

    pe.portfolio_id = request.form['portfolio_id']
    pe.company_id = request.form['company_id']
    pe.price = request.form['price']
    pe.type = request.form['type']
    pe.date = request.form['date']
    pe.count = request.form['count']
    pe.save()
    return redirect('/portfolio')

# End File: stocky/app/controllers/portfolio.py
