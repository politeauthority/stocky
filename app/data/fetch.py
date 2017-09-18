"""Fetch

Usage:
    fetch.py [options]

Options:
    --one_year          Get 365 day data on for all companies in the system.
    --daily             Get daily quotes from yahoo.
    --realtime          Runs the new realtime platform.
    --test              Runs some debug tests
    --debug             Run the debugger.

"""
from docopt import docopt
import sys
import os
import requests
from datetime import datetime, timedelta
import dateutil
import csv
from yahoo_finance import Share
# from sqlalchemy.exc import importIntegrityError

sys.path.append("../..")
from app import app
from app.collections import companies as cc
from app.models.quote import Quote
from app.helpers import misc

download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')
download_path = os.path.join(download_path, 'tmp')


def utc_to_mountain(utc_time):
    if isinstance(utc_time, str):
        utc_time = dateutil.parser.parse(utc_time)
    return utc_time.astimezone(dateutil.tz.gettz('America/Denver'))


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
        company.save()


def get_daily_quotes():
    """
    Gets daily quotes for all companies with the Yahoo Stock API.

    """
    app.logger.info('Starting Daily Quotes from Yahoo')
    companies = cc.all()
    total_companies = len(companies)
    count = 0
    for c in companies:
        count += 1
        app.logger.info('(%s/%s) Working on %s' % (count, total_companies, c.name))
        try:
            share = Share(c.symbol)
        except Exception, e:
            app.logger.error('Error getting yahoo stock data for %s, %s' % (c.symbol, e))
            continue
        q = Quote()
        q.company_id = c.id
        q.open = share.data_set['Open']
        q.close = share.get_price()
        q.high = share.get_days_high()
        q.low = share.get_days_low()
        q.volume = share.data_set['Volume']
        if not share.data_set.get('LastTradeDateTimeUTC'):
            app.logger.error('%s No Last trade date' % c.symbol)
            continue
        rounded_quote_date = utc_to_mountain(share.data_set['LastTradeDateTimeUTC']).replace(hour=0)
        q.date = rounded_quote_date
        q.save()
        c.ts_updated = datetime.now()
        c.save()
        app.logger.info('Saved Quote for %s' % c.symbol)


def get_realtime_quotes():
    if misc.markets_open:
        print 'BUY BUY BUY'
    else:
        print 'Markets are closed'


def test():
    x = Quote.query.filter(
        Quote.company_id == 1931 and
        Quote.date >= datetime.now() - timedelta(days=365)).order_by(Quote.high).limit(1).one().high
    print x

if __name__ == "__main__":
    args = docopt(__doc__)

    if args['--one_year']:
        all_company_one_year()
    elif args['--daily']:
        get_daily_quotes()
    elif args['--realtime']:
        get_realtime_quotes()

# End File: stocky/app/data/fetch.py
