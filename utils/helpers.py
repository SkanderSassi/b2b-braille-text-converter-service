from datetime import datetime


def get_current_date(delimiter='-'):
    """Return current year, month, day with delimiter parameter as the delimiter

    Args:
        delimiter (str, optional): separator between year, month and day. Defaults to '-'.

    Returns:
        str: current year, month, day (e.g 2022-04-01) with - as the delimiter
    """
    date = datetime.now()
    curr_date = f"{date.year}{delimiter}{date.month}{delimiter}{date.day}"
    return curr_date
    