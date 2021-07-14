# Updated: 25 Nov 2020

import pytz, traceback
from django.core.exceptions import ValidationError
from datetime import datetime
from scripts.shared import helpers
from growth.models import Fibre2FashionSellingOffer
from relationships.shared import record_email

_NAMESPACE = 'fibre2fashion_selling_offer'

def parse_row(row, import_job):
    
    sgtz = pytz.timezone('Asia/Singapore')
    email_str = helpers.clean_string(row.get('coy_email', None))

    # Record this email
    (email, invalid_email) = record_email(email_str, import_job)
    
    offer, created = Fibre2FashionSellingOffer.objects.get_or_create(
        source_url=helpers.clean_string(row.get('url', None)),
        defaults={
            'harvested': datetime(2020, 2, 29, tzinfo=sgtz) # Set to right date/time
        }
    )

    # Do not override the import_job for updates. We'd know if an entry has
    # been updated if its updated and created timestamps are different.
    if created == True:
        offer.import_job = import_job

    offer.category = helpers.clean_string(row.get('cat', None))
    offer.sub_category = helpers.clean_string(row.get('subcat', None))
    offer.title = helpers.clean_string(row.get('title', None))
    offer.reference_no = helpers.clean_string(row.get('ref_no', None))
    offer.description = helpers.clean_string(row.get('coy_des', None))
    offer.email_str = email_str
    offer.company_name = helpers.clean_string(row.get('coy_name', None))
    offer.company_address = helpers.clean_string(row.get('coy_addr', None))
    offer.product_info_html = helpers.clean_string(row.get('prod_info_html', None))
    offer.email = email
    offer.invalid_email = invalid_email

    try:
        offer.full_clean()
        offer.save()
    except ValidationError:
        traceback.print_exc()
    
def run():
    helpers.load(parse_row, _NAMESPACE)