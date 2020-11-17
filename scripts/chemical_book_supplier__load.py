import os
import boto3
from settings import AWS_STORAGE_BUCKET_NAME

_NAMESPACE_ROOT = '/scripts/namespaces'
_NAMESPACE = 'chemical_book_supplier'
_OBJECT_PREFIX = f'data_transfer/{_NAMESPACE}'
_NUM_FILES = 3

def download_file():
    s3 = boto3.client('s3')
    s3.download_file(AWS_STORAGE_BUCKET_NAME, f'{_OBJECT_PREFIX}/test.txt', 'saved_test.txt')

def parse_file():
    pass

def delete_file():
    pass

def load_files():
    pass

if __name__ == '__main__':
    download_file()
    print(os.listdir())