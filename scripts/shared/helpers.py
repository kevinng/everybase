import os
import inspect
import jsonlines
import csv
import traceback
import boto3
import datetime

from common.models import ImportJob

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

def clean_integer(value):
    if value is None:
        return None

    return int(value)

def clean_boolean(value, true, false):
    if value == true:
        return True
    elif value == false:
        return False
    
    return None

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

def download_object(bucket_name, object_name, filename, namespace):
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
    log_file = os.path.join(namespace,
        f'{inspect.currentframe().f_code.co_name}.log')

    for key in keys:
        print(f'Parsing {key}...')

        filename = key.split('/')[-1] # Remove S3 folder paths in S3
        download_object(key, filename, namespace)
        (_, rows) = read_file(filename, namespace)
        for row in rows:
            try:
                parse_row(row)
            except Exception as e:
                traceback.print_exc()
                log(log_file, row, e)
        delete_file(filename, namespace)

def import_namespace(parse_row, namespace):
    prefix = f'{_DATA_TRANSFER_REMOTE_PATH}/{namespace}/'
    keys = get_object_keys(prefix)
    parse_objects(keys, parse_row, namespace)

def load(parse_row, namespace):
    # New import job
    import_job = ImportJob(
        status='started',
        description=f'Namespace: {namespace}'
    )
    import_job.save()

    # Preset import job for parse_row function
    preset_parse_row = lambda row: parse_row(row, import_job)

    failed = False
    try:
        import_namespace(preset_parse_row, namespace)
    except Exception:
        traceback.print_exc()

        # Update import job status
        import_job.status = 'failed'
        import_job.save()

        failed = True

    if failed == False:
        # Update import job status
        import_job.status = 'succeeded'
        import_job.save()