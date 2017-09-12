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


# End File: stocky/app/controllers/portfolio.py
