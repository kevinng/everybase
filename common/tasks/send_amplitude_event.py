import pytz, datetime, requests
from celery import shared_task
from everybase import settings

@shared_task
def send_amplitude_event(
        event_type : str,
        user_id : int = None,
        device_id : str = None,
        session_id : str = None,
        event_properties : dict = None,
        user_properties : dict = None,
        app_version : str = None,
        platform : str = None,
        os_name : str = None,
        os_version : str = None,
        device_brand : str = None,
        device_manufacturer : str = None,
        device_model : str = None,
        carrier : str = None,
        country : str = None,
        region : str = None,
        city : str = None,
        dma : str = None,
        language : str = None,
        price : str = None,
        quantity : str = None,
        revenue : str = None,
        product_id : str = None,
        revenue_type : str = None,
        location_lat : str = None,
        location_lng : str = None,
        ip : str = None,
        idfa : str = None,
        idfv : str = None,
        adid : str = None,
        android_id : str = None
    ):
    if settings.AMPLITUDE_API_KEY is None or \
        settings.AMPLITUDE_API_KEY.strip() == '':
        return None

    # Current time
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    epoch = sgtz.localize(datetime.datetime(1970, 1, 1))
    now_epoch = int((now - epoch).total_seconds())

    # Amplitude posting function
    def post_amplitude():
        e = {'time': now_epoch}
        
        if user_id is not None:
            e['user_id'] = user_id
        
        if session_id is not None:
            e['session_id'] = session_id

        if device_id is not None:
            e['device_id'] = device_id

        if event_type is not None:
            e['event_type'] = event_type

        if event_properties is not None:
            e['event_properties'] = event_properties

        if user_properties is not None:
            e['user_properties'] = user_properties

        if app_version is not None:
            e['app_version'] = app_version

        if platform is not None:
            e['platform'] = platform

        if os_name is not None:
            e['os_name'] = os_name

        if os_version is not None:
            e['os_version'] = os_version

        if device_brand is not None:
            e['device_brand'] = device_brand

        if device_manufacturer is not None:
            e['device_manufacturer'] = device_manufacturer

        if device_model is not None:
            e['device_model'] = device_model

        if carrier is not None:
            e['carrier'] = carrier

        if country is not None:
            e['country'] = country

        if region is not None:
            e['region'] = region

        if city is not None:
            e['city'] = city

        if dma is not None:
            e['dma'] = dma

        if language is not None:
            e['language'] = language

        if price is not None:
            e['price'] = price

        if quantity is not None:
            e['quantity'] = quantity

        if revenue is not None:
            e['revenue'] = revenue

        if product_id is not None:
            e['productId'] = product_id

        if revenue_type is not None:
            e['revenueType'] = revenue_type

        if location_lat is not None:
            e['location_lat'] = location_lat

        if location_lng is not None:
            e['location_lng'] = location_lng

        if ip is not None:
            e['ip'] = ip

        if idfa is not None:
            e['idfa'] = idfa

        if idfv is not None:
            e['idfv'] = idfv

        if adid is not None:
            e['adid'] = adid

        if android_id is not None:
            e['android_id'] = android_id

        return requests.post('https://api2.amplitude.com/2/httpapi', json={
            'api_key': settings.AMPLITUDE_API_KEY,
            'events': [e]
        })

    # Retry once if failed.
    r = post_amplitude()
    if r.status_code != 200:
        r = post_amplitude()
    
    return r