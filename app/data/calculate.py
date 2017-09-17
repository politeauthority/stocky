"""Fetch

Usage:
    fetch.py [options]

Options:
    --test
    --debug             Run the debugger.

"""
from docopt import docopt
import sys
import os
import requests
from datetime import datetime, timedelta
from yahoo_finance import Share

sys.path.append("../..")
from app import app
from app.collections import companies as cc
from app.models.company import Company
from app.models.quote import Quote


def update_company_52_week_data():
    """
    """
    companeis = cc.all()
    total = len(compnies)
    count = 0
    for c in companies:
        count += 1
        app.logger.info('(%s/%s) Processing %s ' % (count, total, c.name))
        52_week_low = Quote.query.filter().order_by(Quote.low).limit(1).one().high
        print 52_week_high
        # print 52_week_low

if __name__ == "__main__":
    args = docopt(__doc__)
    update_company_52_week_data()

# End File: stocky/app/data/calculate.py
