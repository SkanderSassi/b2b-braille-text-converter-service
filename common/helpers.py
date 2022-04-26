from datetime import datetime
from common.exceptions import *
from werkzeug.utils import secure_filename


def get_secure_filename(filename):
    filename_secure = secure_filename(filename)
    if not filename_secure:
        raise EmptyFileName("Empty filename")
    return filename_secure

def check_filetype_allowed(filetype, allowed_types):
    if filetype not in allowed_types:
        raise FileTypeNotAllowed(
            f"The specified file type is not allowed, allowed file types : {allowed_types}",
            filetype,
        )
def get_request_data(request_data):
    extension = request_data["to_type"]
    filename = request_data["filename"]
    content = request_data["pages"]
    translation_table = request_data["translation_table"]
    return extension, filename, content, translation_table

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
    