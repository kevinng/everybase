import pytz, datetime, requests, hashlib
from celery import shared_task

from everybase import settings
from amplitude import models
from relationships import models as relmods

@shared_task
def send_event(
        user_id: int,
        event_type: str,
        device_id: str = None,
        event_properties: dict = None,
        user_properties: dict = None,
        app_version: str = None,
        platform: str = None,
        os_name: str = None,
        os_version: str = None,
        device_brand: str = None,
        device_manufacturer: str = None,
        device_model: str = None,
        carrier: str = None,
        country: str = None,
        region: str = None,
        city: str = None,
        dma: str = None,
        language: str = None,
        price: str = None,
        quantity: str = None,
        revenue: str = None,
        product_id: str = None,
        revenue_type: str = None,
        location_lat: str = None,
        location_lng: str = None,
        ip: str = None,
        idfa: str = None,
        idfv: str = None,
        adid: str = None,
        android_id: str = None
    ):
    if settings.AMPLITUDE_API_KEY is None or \
        settings.AMPLITUDE_API_KEY.strip() == '':
        return None

    # Current time
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    epoch = sgtz.localize(datetime.datetime(1970, 1, 1))
    now_epoch = int((now - epoch).total_seconds())

    # User's session, if any
    session = models.Session.objects\
        .filter(user=user_id)\
        .order_by('-last_activity')\
        .first()

    # Elapsed session time - if any
    if session is not None:
        session_id = session.session_id
    else:
        session_id = -1 # No session ID

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

    # Get user's uuid - we post the user's key instead of the user's ID because
    # Amplitude has a 5-char minimum on their user ID
    user = relmods.User.objects.get(pk=user_id)

    # Post to Amplitude
    def post_amplitude():
        return requests.post('https://api2.amplitude.com/2/httpapi', json={
            'api_key': settings.AMPLITUDE_API_KEY,
            'events': [{
                'user_id': user.uuid,
                'device_id': device_id,
                'event_type': event_type,
                'time': now_epoch,
                'event_properties': event_properties,
                'user_properties': user_properties,
                'app_version': app_version,
                'platform': platform,
                'os_name': os_name,
                'os_version': os_version,
                'device_brand': device_brand,
                'device_manufacturer': device_manufacturer,
                'device_model': device_model,
                'carrier': carrier,
                'country': country,
                'region': region,
                'city': city,
                'dma': dma,
                'language': language,
                'price': price,
                'quantity': quantity,
                'revenue': revenue,
                'productId': product_id,
                'revenueType': revenue_type,
                'location_lat': location_lat,
                'location_lng': location_lng,
                'ip': ip,
                'idfa': idfa,
                'idfv': idfv,
                'adid': adid,
                'android_id': android_id,
                'event_id': hash, # To prevent duplicates
                'session_id': session_id,
                'insert_id': hash # To prevent duplicates
            }]
        })

    r = post_amplitude()
    if r.status_code != 200:
        # Retry once if failed.
        r = post_amplitude()

    # Save entry
    return models.Event.objects.create(
        requested=now,
        responded=datetime.datetime.now(tz=sgtz),
        response_code=r.status_code,
        response_text=r.text,
        user_id=user.id,
        device_id=device_id,
        event_type=event_type,
        time_dt=now,
        time=now_epoch,
        app_version=app_version,
        platform=platform,
        os_name=os_name,
        os_version=os_version,
        device_brand=device_brand,
        device_manufacturer=device_manufacturer,
        device_model=device_model,
        carrier=carrier,
        country=country,
        region=region,
        city=city,
        dma=dma,
        language=language,
        price=price,
        quantity=quantity,
        revenue=revenue,
        product_id=product_id,
        revenue_type=revenue_type,
        location_lat=location_lat,
        location_lng=location_lng,
        ip=ip,
        idfa=idfa,
        idfv=idfv,
        adid=adid,
        android_id=android_id,
        event_id=hash,
        session_id=session_id,
        insert_id=hash
    )