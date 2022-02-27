from common.utilities.diff_now import diff_now

def diff_now_desc(past):
    weeks, days, hours, minutes, seconds = diff_now(past)

    if weeks >= 1 and weeks <= 2:
        return '%dw ago' % weeks
    elif weeks < 1:
        if days >= 1:
            return '%dd ago' % days
        elif days < 1:
            if hours >= 1:
                return '%dh ago' % hours
            elif hours < 1:
                if minutes >= 1:
                    return '%dm ago' % minutes
                elif minutes < 1:
                    return '%ds ago' % seconds

    return past.strftime('%d %b %y')