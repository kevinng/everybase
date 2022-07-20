import requests, json
from celery import shared_task
from everybase import settings

@shared_task
def identify_amplitude_user(user_id, user_properties):
    if settings.AMPLITUDE_API_KEY is None or \
        settings.AMPLITUDE_API_KEY.strip() == '':
        return None

    user_properties_str = str(json.dumps(user_properties))
    
    def post_amplitude():
        return requests.post(settings.AMPLITUDE_IDENTIFY_URL, headers={}, files=[], data={
            'api_key': settings.AMPLITUDE_API_KEY,
            'identification': f'[{{"user_id":"{str(user_id)}","user_properties":{user_properties_str}}}]'
        })

    # Retry once if failed.
    r = post_amplitude()
    if r.status_code != 200:
        r = post_amplitude()
    
    return r