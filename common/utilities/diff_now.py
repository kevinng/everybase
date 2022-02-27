import pytz, datetime
from everybase import settings

def diff_now(past):
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    difference = (now - past).total_seconds()
    
    weeks, rest = divmod(difference, 604800)
    days, rest = divmod(rest, 86400)
    hours, rest = divmod(rest, 3600)
    minutes, seconds = divmod(rest, 60)

    return (weeks, days, hours, minutes, seconds)