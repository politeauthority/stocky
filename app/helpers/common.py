"""Helpers Common

"""


def get_percentage(partial, total, rounding=2):
    """
        @desc
            basic percentage calculator
        @param
            partial  : int() or float() 25
            total    : int() or float()  100
            rounding : int()
        @return
            float()
    """
    partial = float(partial)
    total = float(total)
    return round(partial * 100 / total, rounding)

# End File stocky/app/helpers/common.py
