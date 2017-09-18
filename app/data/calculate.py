"""Calculate

Usage:
    calculate.py [options]

Options:
    --test
    --debug             Run the debugger.

"""
from docopt import docopt
import sys
from datetime import datetime, timedelta

sys.path.append("../..")
from app import app
from app.collections import companies as cc
from app.models.quote import Quote


def update_company_52_week_data():
    """
    """
    companeis = cc.all()
    total = len(companeis)
    count = 0
    for c in companeis:
        count += 1
        app.logger.info('(%s/%s) Processing %s ' % (count, total, c.name))
        low_52 = Quote.query.filter(
            Quote.company_id == c.id,
            Quote.date >= datetime.now() - timedelta(days=365)).order_by(Quote.low).limit(1).one().high
        print low_52

if __name__ == "__main__":
    args = docopt(__doc__)
    update_company_52_week_data()

# End File: stocky/app/data/calculate.py
