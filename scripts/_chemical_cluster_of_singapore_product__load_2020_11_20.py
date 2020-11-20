import pytz
from datetime import datetime
from .shared import helpers
from growth.models import ChemicalClusterOfSingaporeProduct

_NAMESPACE = 'chemical_cluster_of_singapore_product'

def parse_row(row, import_job):

    product = ChemicalClusterOfSingaporeProduct(
        import_job=import_job,
        harvested=datetime.now(pytz.timezone('Asia/Singapore')), # Wrong
        source_url=helpers.clean_string(row.get('url', None)),
        company_name=helpers.clean_string(row.get('name', None)),
        product=helpers.clean_string(row.get('product', None))
    )
    product.full_clean()
    product.save()
    
def run():
    helpers.load(parse_row, _NAMESPACE)