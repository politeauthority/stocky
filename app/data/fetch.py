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
from yahoo_finance import Share
from bs4 import BeautifulSoup

sys.path.append("../..")
from app import app
from app.collections import companies as cc
from app.models.quote import Quote
from app.helpers import misc_time

from modules import google_quotes

download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')
download_path = os.path.join(download_path, 'tmp')


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
        # calculate_company_stats(company)
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


def get_realtime_quotes():
    """
    Not built yet.

    """
    return None


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


if __name__ == "__main__":
    args = docopt(__doc__)

    if args['--one_year']:
        google_quotes.all_company_one_year()
    elif args['--daily']:
        get_daily_quotes()
    elif args['--realtime']:
        get_realtime_quotes()
    elif args['--dividends']:
        dividends()
    elif args['--test']:
        test()

# End File: stocky/app/data/fetch.py
