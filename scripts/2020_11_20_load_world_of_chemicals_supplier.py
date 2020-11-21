import pytz
from datetime import datetime
from .shared import helpers
from growth.models import WorldOfChemicalsSupplier

_NAMESPACE = 'world_of_chemicals_supplier'

def parse_row(row, import_job):

    coy_email = helpers.clean_string(row.get('coy_email', None))
    (email, invalid_email) = helpers.record_email(coy_email, import_job)

    coy_owner_email = helpers.clean_string(row.get('coy_owner_email', None))
    (owner_email, invalid_owner_email) = helpers.record_email(
        coy_owner_email, import_job)

    coy_alt_email = helpers.clean_string(row.get('coy_alt_email', None))
    (alt_email, invalid_alt_email) = helpers.record_email(coy_alt_email,
        import_job)

    coy_alt_email_2 = helpers.clean_string(row.get('coy_alt_email_2', None))
    (alt_email_2, invalid_alt_email_2) = helpers.record_email(coy_alt_email_2,
        import_job)

    coy_alt_email_3 = helpers.clean_string(row.get('coy_alt_email_3', None))
    (alt_email_3, invalid_alt_email_3) = helpers.record_email(coy_alt_email_3,
        import_job)

    supplier = WorldOfChemicalsSupplier(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')), # Wrong
        source_url=helpers.clean_string(row.get('source_url', None)),
        coy_id=helpers.clean_string(row.get('coy_id', None)),
        coy_name=helpers.clean_string(row.get('coy_name', None)),
        coy_about_html=helpers.clean_string(row.get('coy_about_html', None)),
        coy_pri_contact=helpers.clean_string(row.get('coy_pri_contact', None)),
        coy_addr_1=helpers.clean_string(row.get('coy_addr_1', None)),
        coy_addr_2=helpers.clean_string(row.get('coy_addr_2', None)),
        coy_city=helpers.clean_string(row.get('coy_city', None)),
        coy_state=helpers.clean_string(row.get('coy_state', None)),
        coy_country=helpers.clean_string(row.get('coy_country', None)),
        coy_postal=helpers.clean_string(row.get('coy_postal', None)),
        coy_phone=helpers.clean_string(row.get('coy_phone', None)),
        coy_phone_2=helpers.clean_string(row.get('coy_phone_2', None)),
        coy_email=coy_email,
        coy_owner_email=coy_owner_email,
        coy_alt_email=coy_alt_email,
        coy_alt_email_2=coy_alt_email_2,
        coy_alt_email_3=coy_alt_email_3,
        coy_website=helpers.clean_string(row.get('coy_website', None)),
        email=email,
        owner_email=owner_email,
        alt_email=alt_email,
        alt_email_2=alt_email_2,
        alt_email_3=alt_email_3,
        invalid_email=invalid_email,
        invalid_owner_email=invalid_owner_email,
        invalid_alt_email=invalid_alt_email,
        invalid_alt_email_2=invalid_alt_email_2,
        invalid_alt_email_3=invalid_alt_email_3
    )
    supplier.full_clean()
    supplier.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)