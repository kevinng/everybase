import requests
from typing import Dict
from celery import shared_task

@shared_task
def copy_post_request_data(
        url: str,
        data: Dict
    ):
    requests.post(url, data=data)