"""Company - Controller

"""

from flask import Blueprint, render_template, request, redirect

from app.models.company import Company, CompanyDividend
from app.collections import companies as cc
from app.helpers.decorators import requires_auth

admin = Blueprint('Admin', __name__, url_prefix='/admin')


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


@admin.route('/dividend/form')
@requires_auth
def form_dividend():
    """
    Form to add a new dividend.

    """
    d = {
        'companies': cc.all('symbol')
    }
    return render_template('admin/add_dividend.html', **d)


@admin.route('/dividend/add', methods=['POST'])
@requires_auth
def add_dividend():
    """
    Form to add a new dividend.

    """
    company = Company(request.form['dividend_company_id'])
    dividend = CompanyDividend()
    dividend.company_id = company.id
    dividend.eff_date = request.form['dividend_eff_date']
    dividend.declaration_date = request.form['dividend_declaration_date']
    dividend.record_date = request.form['dividend_record_date']
    dividend.pay_date = request.form['dividend_pay_date']
    dividend.price = request.form['dividend_price']
    dividend.save()
    company.save()
    return redirect('/company/%s' % company.symbol)

# End File: stocky/app/controllers/admin.py
