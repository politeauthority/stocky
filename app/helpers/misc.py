"""Misc - Helpers

"""

from datetime import datetime
import holidays


def markets_open(time_to_check=None, just_the_date=False):
    """
    Determines if markets are currently open, or open by defined by the date supplied.

    :param check_time: Datetime future or present.
    :type check_time: Datetime
    :param just_the_date: To just check if markets were open on that date, not by time.
    :type just_the_date: bool
    :return: The markets are open or not.
    :rtype: bool
    """

    if time_to_check:
        the_time = time_to_check
    else:
        the_time = datetime.now()

    if the_time.weekday() in [4, 5]:
        print 'weekday'
        return False

    us_holidays = holidays.UnitedStates()

    if the_time in us_holidays:
        return False

    if not just_the_date:
        if the_time.hour + 2 < 9:
            return False
        if the_time.hour + 2 > 17:
            return False
    return True
