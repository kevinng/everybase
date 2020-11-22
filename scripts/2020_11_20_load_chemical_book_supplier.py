import pytz
from datetime import datetime
from .shared import helpers
from growth.models import ChemicalBookSupplier
from relationships.shared import record_email

_NAMESPACE = 'chemical_book_supplier'

def parse_row(row, import_job):

    email_str = helpers.clean_string(row.get('coy_email', None))

    # Record this email
    (email, invalid_email) = record_email(email_str, import_job)

    supplier = ChemicalBookSupplier(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')), # Wrong
        source_url=helpers.clean_string(row.get('source_url', None)),
        company_name=helpers.clean_string(row.get('coy_name', None)),
        internal_url=helpers.clean_string(row.get('coy_internal_href', None)),
        telephone=helpers.clean_string(row.get('coy_tel', None)),
        email_str=email_str,
        corporate_site_url=helpers.clean_string(row.get('coy_href', None)),
        nationality=helpers.clean_string(row.get('coy_nat', None)),
        email=email,
        invalid_email=invalid_email
    )
    supplier.full_clean()
    supplier.save()

def run():
    helpers.load(parse_row, _NAMESPACE)