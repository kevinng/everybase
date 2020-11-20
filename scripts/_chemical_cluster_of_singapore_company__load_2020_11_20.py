import pytz
from datetime import datetime
from .shared import helpers
from growth.models import ChemicalClusterOfSingaporeCompany

_NAMESPACE = 'chemical_cluster_of_singapore_company'

def parse_row(row, import_job):

    # Email
    email_str = helpers.clean_string(row.get('email', None))
    (email, invalid_email) = helpers.record_email(email_str, import_job)

    # Executive email
    executive_email_str = helpers.clean_string(row.get('executive_email', None))
    (executive_email, invalid_executive_email) = helpers.record_email(
        executive_email_str, import_job)

    company = ChemicalClusterOfSingaporeCompany(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')),
        source_url=helpers.clean_string(row.get('url', None)),
        company_name=helpers.clean_string(row.get('name', None)),
        telephone=helpers.clean_string(row.get('tel', None)),
        fax=helpers.clean_string(row.get('fax', None)),
        email_str=email_str,
        website=helpers.clean_string(row.get('web', None)),
        address=helpers.clean_string(row.get('address', None)),
        nature_of_business=helpers.clean_string(
            row.get('nature_of_business', None)),
        executive_name=helpers.clean_string(row.get('executive_name', None)),
        executive_telephone=helpers.clean_string(
            row.get('executive_tel', None)),
        executive_email_str=executive_email_str,
        email=email,
        invalid_email=invalid_email,
        executive_email=executive_email,
        invalid_executive_email=invalid_executive_email
    )

    company.full_clean()
    company.save()

def run():
    helpers.load(parse_row, _NAMESPACE)