"""Google Quotes

"""
import os
import sys
import time
from datetime import datetime, timedelta
import csv

import requests
from sqlalchemy.orm.exc import NoResultFound

sys.path.append("../../..")
from app import app
from app.collections import companies as cc
from app.models.quote import Quote
from app.helpers import common
from app.helpers import calculations


download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')
download_path = os.path.join(download_path, 'tmp')


def all_company_one_year(symbols):
    """
    Google provides a 365 day csv of stock prices publicly. This is how we do it.

    """
    if not symbols:
        companies = cc.all()
    elif 'watchlist' in symbols:
        companies = cc.watchlist()
    else:
        companies = cc.by_symbols(symbols)

    base_url = "https://www.google.com/finance/historical?output=csv&q=%s"

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    # companies = cc.all()

    companies_to_run = len(companies)
    count = 0
    for company in companies:
        count += 1
        app.logger.info("<%s> %s" % (company.symbol, company.name))
        app.logger.info("\tWorking %s/%s" % (count, companies_to_run))

        # Check if we're caught up on this companies quotes.
        quotes_to_fetch = company_missing_quotes(company)
        if not len(quotes_to_fetch):
            app.logger.debug('All caught up on company quotes')
            continue
        app.logger.info('Found %s quotes to save' % len(quotes_to_fetch))

        # Try to fetch the CSV from google
        google_csv_url = base_url % company.symbol
        r = requests.get(google_csv_url)
        if r.status_code == 403:
            app.logger.error('Google thinks were spamming, sending to sleep')
            time.sleep(5)

        if r.status_code != 200:
            app.logger.error('Bad Response: %s from %s' % (r.status_code, google_csv_url))
            continue

        # Write the response to disk
        csv_file = os.path.join(download_path, "%s.csv" % company.symbol)
        app.logger.info('Downloading %s' % csv_file)
        with open(csv_file, 'wb') as f:
            f.write(r.content)

        # Read the Response
        reader = list(csv.DictReader(open(csv_file)))
        c = 0
        app.logger.info('Saving Quotes')
        total_rows = len(reader) - 1
        for row in reader:
            c += 1
            if c == 1:
                continue
            raw_date = datetime.strptime(row['\xef\xbb\xbfDate'], '%d-%b-%y')
            if raw_date not in quotes_to_fetch:
                continue
            raw_open = row['Open']
            raw_high = row['High']
            raw_low = row['Low']
            raw_close = row['Close']
            if len(row) > 5:
                raw_volume = row['Volume']
            else:
                raw_volume = None
            q = Quote()
            q.company_id = company.id
            q.date = raw_date
            if raw_open not in ['-']:
                q.open = raw_open
            if raw_high not in ['-']:
                q.high = raw_high
            if raw_low not in ['-']:
                q.low = raw_low
            q.close = raw_close
            q.volume = raw_volume
            q.save()
            quotes_to_fetch.remove(raw_date)
            if len(quotes_to_fetch) == 0:
                break
            if c % 50 == 0:
                app.logger.info('%s\tProcessed: %s/%s' % (company, c, total_rows))
        calculations.company_flat_stats(company)


def company_missing_quotes(company, days_back=365):
    """
    Gets all the days we have missing quotes for a company.

    :param company: The Company object
    :type company: Company obj
    :param days_back: Number of days back to get days the market was open.
    :type days_back: int
    :return: missing days of quotes to collect.
    :rtype: list
    """
    market_days = market_days_last_year()
    missing_quote_days = market_days
    try:
        quotes = Quote.query.filter(Quote.company_id == company.id).order_by(Quote.date).all()
    except NoResultFound:
        app.logger.warning('%s has no quotes' % company.symbol)
        return []
    for quote in quotes:
        if quote.date in market_days:
            missing_quote_days.remove(quote.date)
    return missing_quote_days


def market_days_last_year(days_back=365):
    """
    Get all days the market was open, from yesterday to however many days back specified.

    :param days_back: Number of days back to get days the market was open.
    :type days_back: int
    :return: All days markets were open
    :rtype: list
    """
    the_days = []
    for x in xrange(1, days_back):
        market_date = datetime.now() - timedelta(days=x)
        market_date = market_date.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
        if common.markets_open(market_date, True):
            the_days.append(market_date)
    return the_days
