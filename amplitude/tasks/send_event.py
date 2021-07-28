import pytz, datetime, requests, hashlib
from celery import shared_task

from everybase import settings
from amplitude import models
from relationships import models as relmods

@shared_task
def send_event(
        user_id: int,
        device_id: str,
        event_type: str,
        event_properties: dict,
        user_properties: dict,
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
        android_id: str = None,
        no_external_calls: bool = False
    ):

    # Current time
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    now_epoch = (now - datetime.datetime(1970, 1, 1)).total_seconds()

    # User's session, if any
    session = models.Session.objects\
        .filter(user=user_id)\
        .order_by('-last_activity')\
        .first()

    # Elapsed session time - if any
    if session is not None:
        elapsed_s = (now - session.last_activity).total_seconds()
        timeout_s = int(settings.AMPLITUDE_SESSION_TIMEOUT_SECONDS)

    if session is None or elapsed_s > timeout_s:
        # User has no pre-existing session(s), or the existing one has expired.
        # Create a new one and use its ID.
        new_session = models.Session.objects.create(
            started=now,
            session_id=now_epoch,
            last_activity=now,
            user=user_id
        )

        session_id = new_session.session_id
    else:
        # Session has not expired, use its ID and update its last activity time
        session.last_activity = now
        session.save()

        session_id = session.session_id

    # Create hash for Amplitude's event ID and insert ID
    hash_str = str(user_id) + str(event_type) + str(now)
    hash_obj = hashlib.md5(hash_str.encode())
    hash = hash_obj.hexdigest()

    # Get user's key - we post the user's key instead of the user's ID because
    # Amplitude has a 5-char minimum on their user ID
    user = relmods.User.objects.get(pk=user_id)

    # Post to Amplitude
    def post_amplitude():
        return requests.post('https://api2.amplitude.com/2/httpapi', params={
            'user_id': user.key,
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
            'event_id': hash,
            'session_id': session_id,
            'insert_id': hash
        }, headers={
            'Content-Type': 'application/json',
            'Accept': '*/*'
        })

    if no_external_calls != True:
        r = post_amplitude()
        if r.status_code != 200:
            # Retry once if failed
            r = post_amplitude()

    # Save entry
    return models.Event.objects.create(
        requested=now,
        responded=datetime.datetime.now(tz=sgtz),
        response_code=r.status_code if no_external_calls == False else None,
        user_id=user.key,
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