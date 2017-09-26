"""Portfolio - CONTROLLER

"""

from flask import Blueprint, render_template, request, redirect

from app.models.portfolio import PortfolioEvent

portfolio = Blueprint('Portfolio', __name__, url_prefix='/portfolio')


@portfolio.route('')
def index():
    """
    Portfolio Index page

    """
    return render_template('portfolio/index.html')


@portfolio.route('/event/form')
def form_event():
    return render_template('portfolio/add_event.html')


@portfolio.route('/event/add', methods=['POST'])
def add_event():
    pe = PortfolioEvent()

    pe.portfolio_id = request.form['portfolio_id']
    pe.company_id = request.form['company_id']
    pe.price = request.form['price']
    pe.type = request.form['type']
    pe.date = request.form['date']
    pe.save()
    return redirect('/portfolio')

# End File: stocky/app/controllers/portfolio.py
