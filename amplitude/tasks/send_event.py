import pytz, datetime, requests, hashlib
from celery import shared_task
from requests.sessions import session

from everybase import settings
from amplitude import models
from relationships import models as relmods

@shared_task
def send_event(
        event_type : str,
        user_pk : int = None,
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

    # Get user's uuid - we post the user's key instead of the user's ID because
    # Amplitude has a 5-char minimum on their user ID. Do this only if the user
    # is authenticated. If the user is not authenticated, do not send in the
    # user ID.
    if user_pk is not None:
        user = relmods.User.objects.get(pk=user_pk)
        # Use UUID to meet Amplitude minimum character count for user ID
        user_id = user.uuid
    else:
        user_id = None

    # Create hash for Amplitude's event ID and insert ID.
    #
    # event ID:
    # (Optional) An incrementing counter to distinguish events with the same
    # user_id and timestamp from each other. We recommend you send an event_id,
    # increasing over time, especially if you expect events to occur
    # simultanenously.
    #
    # insert ID:
    # (Optional) A unique identifier for the event. We will deduplicate
    # subsequent events sent with an insert_id we have already seen before
    # within the past 7 days. We recommend generation a UUID or using some
    # combination of device_id, user_id, event_type, event_id, and time.
    hash_str = str(user_id) + str(event_type) + str(now)
    hash_obj = hashlib.md5(hash_str.encode('utf-8'))
    hash = int(hash_obj.hexdigest(), 16) % (10 ** 8)

    # Amplitude posting function
    def post_amplitude():
        e = {'time': now_epoch,
            'event_id': hash,
            'insert_id': hash}

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

    # Save entry
    event = models.Event(
        requested=now,
        responded=now,
        event_id=hash,
        insert_id=hash,
        time_dt=now,
        time=now_epoch,
        response_code=r.status_code,
        response_text=r.text
    )

    if user_id is not None:
        event.user_id = user.id
    
    if session_id is not None:
        event.session_id = session_id
    
    if device_id is not None:
        event.device_id = device_id

    if event_type is not None:
        event.event_type = event_type

    if app_version is not None:
        event.app_version = app_version

    if platform is not None:
        event.platform = platform

    if os_name is not None:
        event.os_name = os_name

    if os_version is not None:
        event.os_version = os_version

    if device_brand is not None:
        event.device_brand = device_brand

    if device_manufacturer is not None:
        event.device_manufacturer = device_manufacturer

    if device_model is not None:
        event.device_model = device_model

    if carrier is not None:
        event.carrier = carrier

    if country is not None:
        event.country = country

    if region is not None:
        event.region = region

    if city is not None:
        event.city = city

    if dma is not None:
        event.dma = dma

    if language is not None:
        event.language = language

    if price is not None:
        event.price = price

    if quantity is not None:
        event.quantity = quantity

    if revenue is not None:
        event.revenue = revenue

    if product_id is not None:
        event.product_id = product_id

    if revenue_type is not None:
        event.revenue_type = revenue_type

    if location_lat is not None:
        event.location_lat = location_lat

    if location_lng is not None:
        event.location_lng = location_lng

    if ip is not None:
        event.ip = ip

    if idfa is not None:
        event.idfa = idfa

    if idfv is not None:
        event.idfv = idfv

    if adid is not None:
        event.adid = adid

    if android_id is not None:
        event.android_id = android_id

    return event.save()