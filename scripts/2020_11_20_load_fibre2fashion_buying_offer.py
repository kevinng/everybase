import pytz
from datetime import datetime
from .shared import helpers
from growth.models import Fibre2FashionBuyingOffer
from relationships.shared import record_email

_NAMESPACE = 'fibre2fashion_buying_offer'

def parse_row(row, import_job):

    email_str = helpers.clean_string(row.get('coy_email', None))

    # Record this email
    (email, invalid_email) = record_email(email_str, import_job)

    offer = Fibre2FashionBuyingOffer(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')), # Wrong
        source_url=helpers.clean_string(row.get('url', None)),
        category=helpers.clean_string(row.get('cat', None)),
        sub_category=helpers.clean_string(row.get('subcat', None)),
        title=helpers.clean_string(row.get('title', None)),
        reference_no=helpers.clean_string(row.get('ref_no', None)),
        description=helpers.clean_string(row.get('coy_des', None)),
        email_str=email_str,
        product_info_html=helpers.clean_string(row.get('prod_info_html', None)),
        email=email,
        invalid_email=invalid_email
    )
    offer.full_clean()
    offer.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)