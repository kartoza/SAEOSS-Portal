from datetime import datetime


def parse_date_time(date_stamp):
    """A helper method to create a date object from a CBERS time stamp.

    :param date_stamp: Date in this format:
    :type date_stamp: str

    Example format from CBERS:`2015-12-03 10:40:23`

    :returns: A python datetime object.
    :rtype: datetime
    """
    # print 'Parsing Date: %s\n' % date_stamp
    start_year = date_stamp[0:4]
    start_month = date_stamp[5:7]
    start_day = date_stamp[8:10]
    start_time = date_stamp[11:19]
    tokens = start_time.split(':')
    start_hour = tokens[0]
    start_minute = tokens[1]
    start_seconds = tokens[2]

    parsed_date_time = datetime(
        int(start_year),
        int(start_month),
        int(start_day),
        int(start_hour),
        int(start_minute),
        int(start_seconds))
    return parsed_date_time
