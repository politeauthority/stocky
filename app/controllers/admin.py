"""Company - Controller

"""

from flask import Blueprint, render_template, request, redirect

from app.models.company import Company
from app.helpers.decorators import requires_auth

admin = Blueprint('Admin', __name__, url_prefix='/admin')


@admin.route('')
@requires_auth
def index():
    """
    Admin Index

    """
    return render_template('admin/index.html')


@admin.route('/company/form')
@requires_auth
def form_company():
    """
    Form to add a new company.

    """
    return render_template('admin/add_company.html')


@admin.route('/company/add', methods=['POST'])
@requires_auth
def add_company():
    """
    Method to save new company.

    """
    company = Company()
    company.name = request.form['company_name']
    company.symbol = request.form['company_symbol']
    company.ipo_year = request.form['company_ipo_date']
    company.sector = request.form['company_sector']
    company.industry = request.form['company_industry']
    company.save()
    return redirect('/company/%s' % company.symbol)
    return ''
# End File: stocky/app/controllers/company.py
