"""Jinja Filters
"""


def format_currency(value):
    """
    Formats a float or integer to a currency string

    :param value: Value to be manipulated.
    :type value: int or float
    :return: Currency value without symbol.
    :rtype: str
    """
    if not value:
        return ''
    value = round(value, 2)
    value_string = str(value)
    if '.' in value_string:
        x = value_string.find('.')
        if len(value_string[x + 1:]) < 2:
            return value_string + '0'
        elif len(value_string[x + 1:]) < 1:
            return value_string + '00'
    return value_string
