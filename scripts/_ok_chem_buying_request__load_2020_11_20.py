import pytz
from datetime import datetime
from .shared import helpers
from growth.models import OKChemBuyingRequest

_NAMESPACE = 'ok_chem_buying_request'

def parse_row(row, import_job):

    email = helpers.clean_string(row.get('email', None))
    domain = email.split('@')[-1]

    request = OKChemBuyingRequest(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')),
        name=helpers.clean_string(row.get('name', None)),
        country=helpers.clean_string(row.get('country', None)),
        request=helpers.clean_string(row.get('request', None)),
        email=helpers.clean_string(row.get('email', None)),
        domain=domain
    )
    request.full_clean()
    request.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)