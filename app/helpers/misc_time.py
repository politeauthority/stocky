"""
  misc_time
"""
from datetime import datetime
import dateutil.relativedelta


def auto_convert(string_):
    """
        Attempts to automatically figure out the time format being used.
        PLENTY of room for hardening and expanding, but it's going to need to be out
        in the wild for a bit until that's possible.
    """
    print string_
    str_time = str(string_)
    mask = False
    if str_time[4].isdigit():
        if len(str_time) == 10:
            mask = "%Y-%m-%d"
        elif len(str_time == 19):
            mask = '%Y-%m-%d %H:%M:%S'
        elif len(str_time == 23):
            mask = '%Y-%m-%d %H:%M:%S.%f'

    if not mask:
        return False
    try:
        date_obj = datetime.strptime(str_time, mask)
    except ValueError:
        return False
    return date_obj


def ago(the_time):
    """
    Get the time ago string, ie 3 months ago.

    :param the_time: The time in the passed to get the string delta of.
    :type the_time: datetime obj
    """
    if not the_time or not isinstance(the_time, datetime):
        return None
    prefix = ''
    suffix = ''

    if datetime.now() < the_time:
        prefix = 'in'
    else:
        suffix = 'ago'
    rel = dateutil.relativedelta.relativedelta(datetime.now(), the_time)
    unit = None
    value = None
    if rel.years != 0:
        unit = 'years'
        value = rel.years
    elif rel.months != 0:
        unit = 'months'
        value = rel.months
    elif rel.days != 0:
        unit = 'days'
        value = rel.days
    elif rel.hours != 0:
        unit = 'hours'
        value = rel.hours
    elif rel.minutes != 0:
        unit = 'minutes'
        value = rel.minutes
    else:
        unit = 'seconds'
        value = rel.seconds
    if value == 1:
        unit = unit[:-1]
    if '-' in str(value):
        value = str(value).replace('-', '')
    return "%s %s %s %s" % (prefix, value, unit, suffix)


def fmt_date(the_date, fmt=None):
    """
    Formats the date, mostly a jinja template.
    jinja template usage like {{var|fmt_date}}

    :param the_date: The date to get a string from.
    :type the_date: DateTime obk
    :param fmt: Format mask for the date to return in
    :type fmt: str
    :return: String date representation
    :rtype: str
    """
    if not the_date:
        return ''
    if not fmt:
        fmt = '%I:%M:%S %p %b %d %Y'
    return the_date.strftime(fmt)


def utc_to_mountain(utc_time):
    """
    Conerts a UTC Datetime object to Mountain time

    :param utc_time: UTC Datetime object.
    :type utc_time: Datetime obj
    """
    if isinstance(utc_time, str):
        utc_time = dateutil.parser.parse(utc_time)
    return utc_time.astimezone(dateutil.tz.gettz('America/Denver'))
