"""Portfolio - CONTROLLER

"""

from flask import Blueprint, render_template


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


@portfolio.route('/event/add', method=['POST'])
def add_event():
    return render_template('portfolio/add_event.html')

# End File: stocky/app/controllers/portfolio.py
