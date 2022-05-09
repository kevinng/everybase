import requests
from celery import shared_task
from everybase import settings

@shared_task
def identify_amplitude_user(user_id, user_properties):
    if settings.AMPLITUDE_API_KEY is None or \
        settings.AMPLITUDE_API_KEY.strip() == '':
        return None

    # Amplitude posting function
    def post_amplitude():
        return requests.post('https://api2.amplitude.com/identify', json={
            'api_key': settings.AMPLITUDE_API_KEY,
            'user_id': user_id,
            'user_properties': user_properties
        })

    # Retry once if failed.
    r = post_amplitude()
    if r.status_code != 200:
        r = post_amplitude()
    
    return r