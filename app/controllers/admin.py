"""Company - Controller

"""

from flask import Blueprint, render_template, request, redirect
from sqlalchemy.orm.exc import NoResultFound

from app.collections import companies as cc
from app.models.company import Company, CompanyDividend
from app.models.user import User
from app.helpers.decorators import requires_auth


admin = Blueprint('Admin', __name__, url_prefix='/admin')


@admin.route('/company/form')
@admin.route('/company/form/<company_id>')
@requires_auth
def form_company(company_id=None):
    """
    Form to add a new company.

    """
    d = {}
    if company_id:
        try:
            d['edit'] = True
            company = Company.query.filter(Company.id == company_id).one()
            d['company'] = company
        except NoResultFound:
            return render_template('company/404.html'), 404
    return render_template('admin/company_form.html', **d)


@admin.route('/company/save', methods=['POST'])
@requires_auth
def save_company():
    """
    Method to save new company.

    """
    if request.form.get('company_id'):
        company = Company.query.filter(Company.id == request.form.get('company_id')).one()
    else:
        company = Company()
    company.name = request.form['company_name']
    company.symbol = request.form['company_symbol']
    company.ipo_year = request.form['company_ipo_date']
    company.exchange = request.form['company_exchange']
    company.price = request.form['company_price']
    company.ipo_date = request.form['company_ipo_date']
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
    Form to add a new company dividend.

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


@admin.route('/users')
@requires_auth
def users():
    """
    Users roster and management

    """
    users = User.query.all()
    d = {
        'users': users
    }
    return render_template('admin/users.html', **d)


@admin.route('/user/form')
@requires_auth
def form_user():
    """
    Form to add a new user.

    """
    d = {
        'companies': cc.all('symbol')
    }
    return render_template('admin/add_user.html', **d)

# End File: stocky/app/controllers/admin.py
