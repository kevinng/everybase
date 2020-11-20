import os
import inspect
import jsonlines
import csv
import traceback
import boto3
import datetime

from common.models import ImportJob
from relationships.models import Email, InvalidEmail

from django.core.exceptions import ValidationError

from everybase.settings import AWS_STORAGE_BUCKET_NAME

_SCRIPTS_ROOT = './scripts'
_LOG_ROOT = f'{_SCRIPTS_ROOT}/logs'
_DATA_TRANSFER_BASE = 'data_transfer'
_DATA_TRANSFER_LOCAL_PATH = f'{_SCRIPTS_ROOT}/{_DATA_TRANSFER_BASE}'
_DATA_TRANSFER_REMOTE_PATH = _DATA_TRANSFER_BASE

def clean_string(value):
    if value is None:
        return None

    return value.strip()

def append_row(path, row):
    with open(path, 'a') as file:
        file.write(row)

def log(filename, *argv):
    path = os.path.join(_LOG_ROOT, filename)
    append_row(path, f'{str(datetime.datetime.now())}\n')
    for arg in argv:
        append_row(path, f'\t{str(arg)}\n')

def get_filetype(filename):
    return filename.split('.')[-1].lower()

def download_object(bucket_name, object_name, out_filename, namespace):
    print(f'Downloading \'{object_name}\' from bucket \'{bucket_name}\'...')

    full_path = os.path.join(_SCRIPTS_ROOT, namespace, filename)
    s3 = boto3.client('s3')
    s3.download_file(AWS_STORAGE_BUCKET_NAME, object_name, full_path)

def delete_file(filename, namespace):
    print(f'Deleting \'{filename}\' from \'{namespace}\'...')

    full_path = os.path.join(_DATA_TRANSFER_LOCAL_PATH, namespace, filename)
    os.remove(full_path)

def read_file(filename, namespace):
    """Read JSON-lines or CSV file into memory.

    Args:
        filename: Name of file to read from within namespace. The extension of
            this name determines the processing filetype.
        namespace: Namespace to locate the file to read.

    Returns:
        If successful - returns tuple (<list of CSV headers - None if not CSV>,
        <list of data rows>). If failed - returns None.
    """
    log_file = os.path.join(namespace,
        f'{inspect.currentframe().f_code.co_name}.log')

    try:
        full_path = os.path.join(_DATA_TRANSFER_LOCAL_PATH, namespace, filename)
        print(f'Reading {full_path} rows into memory...')
        
        filetype = get_filetype(filename)
        rows = []
        if filetype == 'jl':
            with jsonlines.open(full_path) as reader:
                for row in reader:
                    rows.append(row)
            return (None, rows)
        elif filetype == 'csv':
            with open(full_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
                return (reader.fieldnames, rows)
        else:
            log(log_file, 'Unrecognized filetype', full_path, filetype)

    except Exception as e:
        traceback.print_exc()
        log_file = os.path.join(namespace,
            f'{inspect.currentframe().f_code.co_name}.log')
        log(log_file, e)

    return (None, None)

def create_get_email(email, import_job_id=None):
    """Attempt to get an existing email and return its primary key id, or create
    a new email if the input email does not exist.

    Args:
        email: Email address to get, or create if it does not exist.
        import_job: Import job to associate the creation of this email with.

    """
    try:
        return Email.objects.get(email=email).id
    except Email.DoesNotExist:
        pass

    # Will raise an uncaught DoesNotExist error if input import_job_id does
    # not exist
    i = ImportJob.objects.get(pk=import_job_id) \
        if import_job_id is not None else None

    try:
        e = Email(email=email, import_job=i)
        e.full_clean() # Raise error if input email fails validation
        e.save()
        return e.id
    except ValidationError:
        return None

def create_get_invalid_email(email, import_job_id=None):
    """Attempt to get an existing invalid email and return its primary key id,
    or create a new invalid email if the input email does not exist.

    Args:
        email: Invalid email address to get, or create if it does not exist.
        import_job: Import job to associate the creation of this email with.

    """
    try:
        return InvalidEmail.objects.get(email=email).id
    except InvalidEmail.DoesNotExist:
        pass

    # Will raise an uncaught DoesNotExist error if input import_job_id does
    # not exist
    i = ImportJob.objects.get(pk=import_job_id) \
        if import_job_id is not None else None
    
    try:
        e = InvalidEmail(email=email, import_job=i)
        e.full_clean() # Raise error if input email fails validation
        e.save()
        return e.id
    except ValidationError:
        return None

def record_email(email, import_job_id=None):
    """Record email as either an email or an invalid email.

    Args:
        email: Email to record.
        import_job_id: ID of the import job to associate this email with.

    Returns:
        (<email ID or None>, <invalid email ID or None>)
    """
    if email is None or email == '':
        print('None or empty email found')
        return (None, None)

    email_id = create_get_email(email, import_job_id)

    invalid_email_id = None
    if email_id is None:
        invalid_email_id = create_get_invalid_email(email, import_job_id)

    return (email_id, invalid_email_id)

def get_object_keys(prefix):
    # Get object keys with specified prefix
    s3 = boto3.client('s3')
    contents = s3.list_objects(
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Prefix=prefix
    )['Contents']
    
    keys = [content['Key'] for content in contents]

    # Remove the one entry that's exactly equal to prefix (i.e. root folder)
    keys = list(filter(lambda key: key != prefix, keys))

    return keys

def download_object(key, filename, namespace):
    """Download an object from S3 and save it with the output filename within
    the namespace.

    Args:
        key: Full path of the object to download (including 
            folders and the key itself).
        filename: Filename of the file
        namespace: Namespace to save the object in.
    """
    s3 = boto3.client('s3')
    full_path = os.path.join(_DATA_TRANSFER_LOCAL_PATH, namespace, filename)

    s3.download_file(AWS_STORAGE_BUCKET_NAME, key, full_path)

def parse_objects(keys, parse_row, namespace):
    for key in keys:
        filename = key.split('/')[-1] # Remove S3 folder paths in S3
        download_object(key, filename, namespace)
        (_, rows) = read_file(filename, namespace)
        for row in rows:
            parse_row(row)
        delete_file(filename, namespace)

def import_namespace(parse_row, namespace):
    prefix = f'{_DATA_TRANSFER_REMOTE_PATH}/{namespace}/'
    keys = get_object_keys(prefix)
    parse_objects(keys, parse_row, namespace)