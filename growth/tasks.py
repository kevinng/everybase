from celery import shared_task
from everybase.settings import _GMASS_CAMPAIGN_RESULTS_CACHE_PATH
import requests
import os

@shared_task
def load_gmass_campaign_results(id):
    download_url = \
        f'https://www.gmass.co/gmass/downloadcsvaction?C={id}&RT=m'
    
    data = requests.get(download_url).json()['data']
    filename = f'{id}.csv'
    path = os.path.join(_GMASS_CAMPAIGN_RESULTS_CACHE_PATH, filename)

    with open(path, 'w') as file:
        file.write(data)