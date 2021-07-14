# Updated: 20 Nov 2020

import pytz
from datetime import datetime
from scripts.shared import helpers
from growth.models import LookChemSupplier
from relationships.shared import record_email

_NAMESPACE = 'look_chem_supplier'

def parse_row(row, import_job):

    email_str = helpers.clean_string(row.get('coy_email', None))

    # Record this email
    (email, invalid_email) = record_email(email_str, import_job)

    supplier = LookChemSupplier(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')), # Wrong
        company_name=helpers.clean_string(row.get('coy_name', None)),
        contact_person=helpers.clean_string(row.get('contact_person', None)),
        street_address=helpers.clean_string(row.get('street_address', None)),
        city=helpers.clean_string(row.get('city', None)),
        province_state=helpers.clean_string(row.get('province_state', None)),
        country_region=helpers.clean_string(row.get('country_region', None)),
        zip_code=helpers.clean_string(row.get('zip_code', None)),
        business_type=helpers.clean_string(row.get('business_type', None)),
        tel=helpers.clean_string(row.get('tel', None)),
        mobile=helpers.clean_string(row.get('mobile', None)),
        email_str=helpers.clean_string(row.get('email', None)),
        website=helpers.clean_string(row.get('website', None)),
        qq=helpers.clean_string(row.get('qq', None)),
        email=email,
        invalid_email=invalid_email
    )
    supplier.full_clean()
    supplier.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)