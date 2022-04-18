import pytz, datetime
from everybase import settings

def diff_now_in_days(past):
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    difference = (now - past).total_seconds()
    days, _ = divmod(difference, 86400)
    return int(days)