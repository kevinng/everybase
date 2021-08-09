# Updated: 9 Aug 21

import pytz
from datetime import datetime
from scripts.shared import helpers
from growth.models import Fibre2FashionBuyingOffer
from relationships.shared import record_email

_NAMESPACE = 'fibre2fashion_buying_offer'

def parse_row(row, import_job):

    sgtz = pytz.timezone('Asia/Singapore')
    email_str = helpers.clean_string(row.get('coy_email', None))

    # Record this email
    (email, invalid_email) = record_email(email_str, import_job)

    source_url = helpers.clean_string(row.get('url', None))
    
    created = False
    try:
        offer = Fibre2FashionBuyingOffer.objects.get(source_url=source_url)
    except Fibre2FashionBuyingOffer.DoesNotExist:
        offer = Fibre2FashionBuyingOffer.objects.create(
            source_url=source_url,
            import_job=import_job,
            harvested = datetime(2021, 8, 9, tzinfo=sgtz) # Set to right date/time
        )
        created = True

    # Only add details if new
    if created:
        offer.category = helpers.clean_string(row.get('cat', None))
        offer.sub_category = helpers.clean_string(row.get('subcat', None))
        offer.title = helpers.clean_string(row.get('title', None))
        offer.reference_no = helpers.clean_string(row.get('ref_no', None))
        offer.description = helpers.clean_string(row.get('coy_des', None))
        offer.email_str = email_str
        offer.company_name = helpers.clean_string(row.get('coy_name', None))
        offer.product_info_html = helpers.clean_string(row.get('prod_info_html', None))
        offer.email = email
        offer.invalid_email = invalid_email
        offer.save()
        print('Created %d' % offer.id)
    
def run():
    helpers.load(parse_row, _NAMESPACE)