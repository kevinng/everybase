import os
import boto3
from .shared import helpers

from everybase.settings import AWS_STORAGE_BUCKET_NAME

_NAMESPACE = 'chemical_book_supplier'

def parse_row(row):
    # dict_keys(['source_url', 'coy_name', 'coy_internal_href', 'coy_tel', 'coy_email', 'coy_href', 'coy_nat'])

    email = helpers.clean_string(row['coy_email'])
    helpers.record_email(email)


    # Make email nullable
    # UPDATE MODELS WITH NEW FIELD LENGTHS BEFORE ATTEMPTING IMPORT

def run():
    helpers.import_namespace(parse_row, _NAMESPACE)