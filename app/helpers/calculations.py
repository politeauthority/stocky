"""Calculate
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound

sys.path.append("../..")
# from app import app
from app.models.quote import Quote


def company_flat_stats(company):
    """
    Calculate out the last price, and low/high 52 week fields.
    This is generic and can be used by any process at anytime without issue.

    :param company: The company that basic company stats should be calculated for
    :type company: Company obj
    """

    # Get the last quote
    try:
        last_quote = Quote.query.filter(Quote.company_id == company.id).order_by(Quote.date.desc()).limit(1).one()
    except NoResultFound:
        return
    company.price = last_quote.close

    # Get the lows
    quote_filter_args = Quote.company_id == company.id and Quote.date >= datetime.now() - timedelta(days=365)
    low_52_week = Quote.query.filter(quote_filter_args).order_by(Quote.low).limit(1).one()
    company.low_52_weeks = low_52_week.low
    company.low_52_weeks_date = low_52_week.date

    # Get the highs
    high_52_week = Quote.query.filter(quote_filter_args).order_by(Quote.high.desc()).limit(1).one()
    company.high_52_weeks = high_52_week.high
    company.high_52_weeks_date = high_52_week.date
    company.ts_updated = datetime.now()
    company.save()
    return

# End File: stocky/app/data/calculate.py
