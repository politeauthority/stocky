"""Fetch

Usage:
    fetch.py [options]

Options:
    --one_year          Get 365 day data on for all companies in the system.
    --daily             Get daily quotes from yahoo.
    --realtime          Runs the new realtime platform.
    --dividends         Runs the dividends scraper.
    --stock             The symbol to run data jobs against.
    --test              Runs some debug tests.
    --debug             Run the debugger.

"""
from docopt import docopt
import sys
import os
import requests
from datetime import datetime, timedelta
import csv
from sqlalchemy import desc
from yahoo_finance import Share
from bs4 import BeautifulSoup

sys.path.append("../..")
from app import app
from app.collections import companies as cc
from app.models.quote import Quote
from app.helpers import misc
from app.helpers import misc_time

from sqlalchemy.orm.exc import NoResultFound

download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')
download_path = os.path.join(download_path, 'tmp')


def all_company_one_year():
    """
    Google provides a 365 day csv of stock prices publicly. This is how we do it.

    """
    base_url = "https://www.google.com/finance/historical?output=csv&q=%s"

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    companies = cc.all()
    companies_to_run = len(companies)
    count = 0
    for company in companies:
        count += 1
        app.logger.info("<%s> %s" % (company.symbol, company.name))
        app.logger.info("\tWorking %s/%s" % (count, companies_to_run))
        r = requests.get(base_url % company.symbol)
        if r.status_code != 200:
            app.logger.error('Bad Response: %s' % r.status_code)
            continue
        csv_file = os.path.join(download_path, "%s.csv" % company.symbol)
        app.logger.info('Downloading %s' % csv_file)
        with open(csv_file, 'wb') as f:
            f.write(r.content)
        reader = list(csv.DictReader(open(csv_file)))
        c = 0
        app.logger.info('Saving Quotes')
        total_rows = len(reader) - 1
        for row in reader:
            c += 1
            if c == 1:
                continue
            raw_date = datetime.strptime(row['\xef\xbb\xbfDate'], '%d-%b-%y')
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
            if c % 50 == 0:
                app.logger.info('%s\tProcessed: %s/%s' % (company, c, total_rows))
        calculate_company_stats(company)


def get_daily_quotes():
    """
    Gets daily quotes for all companies with the Yahoo Stock API.

    """
    app.logger.info('Starting Daily Quotes from Yahoo')
    companies = cc.all()
    total_companies = len(companies)
    count = 0
    for company in companies:
        count += 1
        app.logger.info('(%s/%s) Working on %s' % (count, total_companies, company.name))
        fetch_stock(company)


def fetch_stock(company):
    """

    """
    quote = handle_yahoo_quote(company)
    if quote:
        app.logger.info('Saved Quote for %s' % company.symbol)
        calculate_company_stats(company)
        app.logger.info('Updated Company info for %s' % company.symbol)


def handle_yahoo_quote(company):
    """
    Gets and saves the current quote for a given company from Yahoo.

    :param company: Company obj
    :type company: obj
    :return The Quote record saved.
    :rtype: Quote
    """
    try:
        share = Share(company.symbol)
    except Exception, e:
        app.logger.error('Error getting yahoo stock data for %s, %s' % (company.symbol, e))
        return False
    q = Quote()
    q.company_id = company.id
    q.open = share.data_set['Open']
    q.close = share.get_price()
    q.high = share.get_days_high()
    q.low = share.get_days_low()
    q.volume = share.data_set['Volume']
    if not share.data_set.get('LastTradeDateTimeUTC'):
        app.logger.error('%s No Last trade date' % company.symbol)
        return False
    rounded_quote_date = misc_time.utc_to_mountain(share.data_set['LastTradeDateTimeUTC']).replace(hour=0)
    q.date = rounded_quote_date
    q.save()
    return q


def calculate_company_stats(company):
    """
    Calculate out the last price, and low/high 52 week fields.
    This is generic and can be used by any fetch process at anytime without issue.


    :param company: The company that basic company stats should be calculated for
    :type company: Company obj
    """
    last_quote = Quote.query.filter(Quote.company_id == company.id).order_by(desc(Quote.date)).limit(1).one()
    company.price = last_quote.close
    quote_filter_args = Quote.company_id == company.id and Quote.date >= datetime.now() - timedelta(days=365)
    low_52_week = Quote.query.filter(quote_filter_args).order_by(Quote.low).limit(1).one()
    high_52_week = Quote.query.filter(quote_filter_args).order_by(desc(Quote.high)).limit(1).one()
    company.low_52_weeks = low_52_week.low
    company.low_52_weeks_date = low_52_week.date
    company.high_52_weeks = high_52_week.high
    company.high_52_weeks_date = high_52_week.date
    company.ts_updated = datetime.now()
    company.save()


def get_realtime_quotes():
    if misc.markets_open:
        print 'BUY BUY BUY'
    else:
        print 'Markets are closed'


def dividends():
    """
    """
    url = "http://www.nasdaq.com/symbol/%s/dividend-history"
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'
    for company in cc.watchlist():
        print url % company.symbol.lower()
        r = requests.get(url, headers={'User-Agent': user_agent})
        print r.text
        soup = BeautifulSoup(r.text, 'html5lib')
        print soup
        exit()


def test():
    companies = cc.watchlist()
    # companies_to_run = len(companies)
    market_days_last_year()
    exit()
    for company in companies:

        print company.symbol
        try:
            quotes = Quote.query.filter(Quote.company_id == company.id).order_by(Quote.date).limit(1).one()
        except NoResultFound:
            app.logger.warning('%s has no quotes' % company.symbol)
            continue
        print quotes.date
        print ''


def market_days_last_year():
    the_days = []
    for x in xrange(0, 10):
        val = datetime.now() - timedelta(days=x)
        print val
        print x
        print misc.markets_open(val, True)
        print ''

if __name__ == "__main__":
    args = docopt(__doc__)

    if args['--one_year']:
        all_company_one_year()
    elif args['--daily']:
        get_daily_quotes()
    elif args['--realtime']:
        get_realtime_quotes()
    elif args['--dividends']:
        dividends()
    elif args['--test']:
        test()

# End File: stocky/app/data/fetch.py
