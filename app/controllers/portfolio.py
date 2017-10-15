"""Portfolio - CONTROLLER

"""

from flask import Blueprint, render_template, request, redirect, session

from app.collections import companies as cc
from app.collections import portfolios as pc
from app.models.portfolio import Portfolio, PortfolioEvent
from app.models.company import Company
from app.helpers.decorators import requires_auth

portfolio = Blueprint('Portfolio', __name__, url_prefix='/portfolio')


@portfolio.route('')
@portfolio.route('/<portfolio_id>')
@requires_auth
def index(portfolio_id=None):
    """
    Portfolio Index page

    """
    portfolios = Portfolio.query.filter(Portfolio.user_id == session['user_id']).all()
    if not portfolio_id and portfolios:
        portfolio_id = portfolios[0].id
    else:
        redirect('/portfolio/form')
    info = pc.by_portfolio(portfolio_id)
    companies = {}
    for company_id in info['companies']:
        companies[company_id] = Company(company_id)
    d = {
        'positions': info['positions'],
        'companies': companies,
        'portfolio': info['portfolio'],
        # 'company_qry': company_qry,
        'totals': info['totals'],
        'portfolios': portfolios
    }
    return render_template('portfolio/index.html', **d)


@portfolio.route('/portfolio/form')
@portfolio.route('/portfolio/form/<portfolio_id>')
@requires_auth
def form_portfolio(portfolio_id=None):
    """
    Form for creating, saving and deleting a Portfolio

    :param portfolio_id: Portforlio.id to be edited or deleted
    :type portfolio_id: int
    """
    d = {}
    d['portfolio'] = None
    d['edit'] = False
    if portfolio_id:
        event = Portfolio().query.filter(Portfolio.id == portfolio_id).one()
        if event:
            d['portfolio'] = event
            d['portfolio'] = True
    return render_template('portfolio/portfolio_form.html', **d)


@portfolio.route('/portfolio/save', methods=['POST'])
@requires_auth
def save_portfolio():
    """
    Save a new or update a PortfolioEvent

    """
    p = Portfolio()
    if request.form.get('id'):
        p.id = request.form['portfolio_id']
    p.name = request.form['portfolio_name']
    p.user_id = session['user_id']
    p.save()
    return redirect('/portfolio')


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
    d['companies'] = cc.all('symbol')
    d['portfolios'] = pc.by_user_id(session['user_id'])
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

    PortfolioEvent.query.filter(PortfolioEvent.id == event_id).delete()
    return redirect('/portfolio')

# End File: stocky/app/controllers/portfolio.py
