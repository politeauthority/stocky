""" Nasdaq Companies
Gets data company data from Nasdaq stocky symbols from the remote server and stores them ion the
stocky comppanies ORM.

"""
import os
import sys
import requests
from datetime import datetime
import csv

sys.path.append("../../..")
from app import app
from app.models.company import Company
from app.helpers import common


download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')
download_path = os.path.join(download_path, 'tmp')


def get_company_data_from_nasdaq():
    philes = __download_nasdaq_public_data()
    __process_nasdaq_public_data_market(philes['nasdaq'], 'nasdaq')
    __process_nasdaq_public_data_market(philes['nyse'], 'nyse')


def __download_nasdaq_public_data():
    """
    Grabs base company data to kick off the database. This should only need to be run once really.

    """
    nasdaq_dir = os.path.join(download_path, 'tmp', 'nasdaq_data')
    if not os.path.exists(nasdaq_dir):
        os.makedirs(nasdaq_dir)
    url_nasdaq = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    url_nyse = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"

    downloaded_files = {}

    app.logger.info('Downloading Nasdaq')
    file_nasdaq = os.path.join(nasdaq_dir, 'nasdaq_%s.csv' % common.file_safe_date(datetime.now()))
    r = requests.get(url_nasdaq)
    with open(os.path.join(download_path, file_nasdaq), 'wb') as code:
        code.write(r.content)
    downloaded_files['nasdaq'] = file_nasdaq

    app.logger.info('Downloading NYSE')
    file_nyse = os.path.join(nasdaq_dir, 'nasdaq_%s.csv' % common.file_safe_date(datetime.now()))
    r = requests.get(url_nyse)
    with open(os.path.join(download_path, file_nyse), 'wb') as code:
        code.write(r.content)
    downloaded_files['nyse'] = file_nyse
    return downloaded_files


def __process_nasdaq_public_data_market(phile, market):
    f = open(phile, 'rb')
    reader = csv.reader(f)
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        vals = {
            'symbol': row[0],
            'name': row[1],
            'last_sale': row[2],
            'market_cap': row[3],
            'ipo_year': row[5],
            'sector': row[6],
            'industry': row[7],
            'exchange': market,
        }
        c = Company.query.filter(
            Company.symbol == vals['symbol'], Company.exchange == market).all()
        if c:
            app.logger.info('Already Have Data for %s' % c[0].name)
            continue
        c = Company()
        c.symbol = vals['symbol']
        c.name = vals['name']
        if vals['last_sale'] != "n/a":
            c.price = vals['last_sale']
        else:
            c.price = 0
        c.market_cap = vals['market_cap']
        c.ipo_year = vals['ipo_year']
        c.sector = vals['sector']
        c.industry = vals['industry']
        c.exchange = vals['exchange']
        c.save()
        app.logger.info('Saved: %s' % c.name)

# End File: stocky/app/data/modules/nasdaq_companies.py
