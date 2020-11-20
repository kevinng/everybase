import os
import boto3
import pytz
import traceback
from datetime import datetime
from .shared import helpers
from common.models import ImportJob
from growth.models import ChemicalBookSupplier
from relationships.models import Email, InvalidEmail
from everybase.settings import AWS_STORAGE_BUCKET_NAME

_NAMESPACE = 'chemical_book_supplier'

def run():
    # Create a new import job to associate with all entries created in this
    # operation
    import_job = ImportJob(
        status='started',
        description=f'Namespace: {_NAMESPACE}'
    )
    import_job.save()

    # Inner function referencing import_job and providing the logic to parse
    # each row
    def parse_row(row):

        email_str = helpers.clean_string(row.get('coy_email', None))

        # Record this email
        (email, invalid_email) = helpers.record_email(email_str, import_job)

        supplier = ChemicalBookSupplier(
            import_job=import_job,
            harvested=datetime.now(pytz.timezone('Asia/Singapore')),
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

    failed = False

    try:
        helpers.import_namespace(parse_row, _NAMESPACE)
    except Exception as e:
        traceback.print_exc()
        print('---')
        print(os.listdir('./'))
        print('---')
        print(os.listdir('/'))

        # Update import job status
        import_job.status = 'failed'
        import_job.save()

        failed = True

    if failed == False:
        # Update import job status
        import_job.status = 'succeeded'
        import_job.save()