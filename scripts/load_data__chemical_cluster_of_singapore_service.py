# Updated: 20 Nov 2020

import pytz
from datetime import datetime
from scripts.shared import helpers
from growth.models import ChemicalClusterOfSingaporeService

_NAMESPACE = 'chemical_cluster_of_singapore_service'

def parse_row(row, import_job):

    service = ChemicalClusterOfSingaporeService(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')), # Wrong
        source_url=helpers.clean_string(row.get('url', None)),
        company_name=helpers.clean_string(row.get('name', None)),
        service=helpers.clean_string(row.get('service', None))
    )
    service.full_clean()
    service.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)