"""Misc - Helpers

"""

from datetime import datetime


def markets_open(check_time=None):
    """
    Determines if markets are currently open, or open by defined by the date supplied.

    :param check_time: Datetime future or present.
    :type check_time:
    :return: The markets are open or not.
    :rtype: bool
    """

    if check_time:
        the_time = check_time
    else:
        the_time = datetime.now()

    if the_time.weekday() in [5, 6]:
        return False

    if the_time.hour + 2 > 9:
        return False
    if the_time.hour > 14:
        return False
    return True
