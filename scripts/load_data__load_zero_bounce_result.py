# Updated: 20 Nov 2020

import pytz
from datetime import datetime
from scripts.shared import helpers
from growth.models import ZeroBounceResult
from relationships.shared import record_email

_NAMESPACE = 'zero_bounce_result'

def parse_row(row, import_job):

    email_str = helpers.clean_string(row.get('Email Address', None))
    (email, invalid_email) = record_email(email_str, import_job)

    did_you_mean = helpers.clean_string(row.get('ZB Did You Mean', None))
    (did_you_mean_email, _) = record_email(did_you_mean, import_job)

    free_email = True if helpers.clean_string(row.get('ZB Free Email', None)) \
        == 'true' else False

    mx_found = True if helpers.clean_string(row.get('ZB MX Found', None)) \
        == 'true' else False

    sgtz = pytz.timezone('Asia/Singapore')

    result = ZeroBounceResult(
        import_job=import_job,
        generated=datetime(2020, 3, 9, tzinfo=sgtz),
        email_str=email_str,
        status=helpers.clean_string(row.get('ZB Status', None)),
        sub_status=helpers.clean_string(row.get('ZB Sub Status', None)),
        account=helpers.clean_string(row.get('ZB Account', None)),
        domain=helpers.clean_string(row.get('ZB Domain', None)),
        first_name=helpers.clean_string(row.get('ZB First Name', None)),
        last_name=helpers.clean_string(row.get('ZB Last Name', None)),
        gender=helpers.clean_string(row.get('ZB Gender', None)),
        free_email=free_email,
        mx_found=mx_found,
        mx_record=helpers.clean_string(row.get('ZB MX Record', None)),
        smtp_provider=helpers.clean_string(row.get('ZB SMTP Provider', None)),
        did_you_mean=did_you_mean,
        email=email,
        invalid_email=invalid_email,
        did_you_mean_email=did_you_mean_email
    )
    result.full_clean()
    result.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)