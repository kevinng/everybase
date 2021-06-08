from chat import models
from chat.libraries import nlp
from relationships import models as relmods
from common import models as commods
import phonenumbers

def get_latest_value(intent_key, message_key, data_key, user):
    """Get latest value captured in context - message_key, intent_key - of a
    data type.

    Parameters
    ----------
    intent_key : string
        Intent key for context
    message_key : string
        Message key for context
    data_key : string
        Data key for data type
    user : relationships.User
        User for whom we're getting a value for
    """
    try:
        # Get latest dataset in context for user
        dataset = models.MessageDataset.objects.filter(
            intent_key=intent_key,
            message_key=message_key,
            user=user.id
        ).order_by('-created').first()
    except models.MessageDataset.DoesNotExist:
        return None

    try:
        # Get value of dataset
        return models.MessageDataValue.objects.get(
            dataset=dataset,
            data_key=data_key
        )
    except models.MessageDataValue.DoesNotExist:
        return None

def get_product_type_with_value(value):
    """Match value against each match keyword with an associated product type
    accounting for edit distance tolerance. If it matches - return the product
    type. If no product type is found - return None.
    
    Parameters
    ----------
    value : string
        Value to match against keywords
    """
    if value is None:
        return None

    match_keywords = commods.MatchKeyword.objects.filter(
        product_type__isnull=False
    )

    for k in match_keywords:
        if nlp.match(value, k.keyword, k.tolerance):
            return k.product_type

    return None

def get_product_type_with_keys(intent_key, message_key, data_key, user):
    """Convenience method to call get_latest_value with inputs for product type
    value and use it to call get_product_type_with_value.

    Parameters
    ----------
    intent_key : string
        Intent key for context
    message_key : string
        Message key for context
    data_key : string
        Data key for data type
    user : relationships.User
        User for whom we're getting the latest value for
    """
    return get_product_type_with_value(
        get_latest_value(intent_key, message_key, data_key, user).\
            value_string)

def get_uom_with_product_type_keys(intent_key, message_key, data_key, user):
    """Convenience method to get product type with get_product_type_with_keys,
    and if it's not null - use it to get the top-priority unit-of-measure
    """
    pt = get_product_type_with_keys(intent_key, message_key, data_key, user)
    if pt is not None:
        try:
            return relmods.UnitOfMeasure.objects.filter(
                product_type=pt
            ).order_by('-priority').first()
        except relmods.UnitOfMeasure.DoesNotExist:
            pass
    
    return None

def save_body_as_string(message, intent_key, message_key, data_key, user):
    """Save message body as a dataset string.

    Parameters
    ----------
    message : TwilioInboundMessage
        Message whose body we're saving
    intent_key : string
        Intent for context we're saving in
    message_key : string
        Message for context we're saving in
    user : relationships.User
        User for whom we're saving the body for
    """
    # TODO: there is a bug there - where a message dataset gets created twice.
    # Since there is a constraint on unique - intent_key/message_key/message,
    # only 1 copy will be created. We'll get an error if we do not use
    # get_or_create.
    dataset, _ = models.MessageDataset.objects.get_or_create(
        intent_key=intent_key,
        message_key=message_key,
        in_message=message,
        user=user
    )

    v = models.MessageDataValue()
    v.value_string = message.body.strip()
    v.dataset = dataset
    v.data_key = data_key
    v.save()

def save_body_as_float(message, intent_key, message_key, data_key, user):
    """Save message body as a dataset float.

    Parameters
    ----------
    message : TwilioInboundMessage
        Message whose body we're saving
    intent_key : string
        Intent for context we're saving in
    message_key : string
        Message for context we're saving in
    user : relationships.User
        User for whom we're saving the body

    Returns
    -------
    Float value if successful, None if unable to convert body to float value
    """
    # TODO: there is a bug there - where a message dataset gets created twice.
    # Since there is a constraint on unique - intent_key/message_key/message,
    # only 1 copy will be created. We'll get an error if we do not use
    # get_or_create.
    dataset, _ = models.MessageDataset.objects.get_or_create(
        intent_key=intent_key,
        message_key=message_key,
        in_message=message,
        user=user
    )

    v = models.MessageDataValue()
    try:
        v.value_float = float(message.body.strip())
    except ValueError:
        return None
    v.dataset = dataset
    v.data_key = data_key
    v.save()

    return v.value_float

def get_phone_number(raw_number):
    """
    Parameters
    ----------
    (phone_number, is_new)
        phone_number - reference to phone number model row
        is_new - True if new phone number was created
    """
    parsed_number = phonenumbers.parse(raw_number, None)

    try:
        # Find phone number
        number = relmods.PhoneNumber.objects.get(
            country_code=parsed_number.country_code,
            national_number=parsed_number.national_number
        )
        return (number, False)
    except relmods.PhoneNumber.DoesNotExist:
        # Create phone number if it doesn't exist
        number = relmods.PhoneNumber(
            country_code=parsed_number.country_code,
            national_number=parsed_number.national_number
        )
        number.save()
        return (number, True)

def get_user(phone_number):
    """
    Parameters
    ----------
    phone_number
        Reference to user's phone number model row

    Returns
    -------
    (user, is_new)
        user - User model row reference
        is_new - True if new user was created, false otherwise.
    """
    try:
        user = relmods.User.objects.get(
            phone_number=phone_number
        )
        return (user, False)
    except relmods.User.DoesNotExist:
        user = relmods.User(
            phone_number=phone_number
        )
        user.save()
        return (user, True)

def get_phone_number_string(twilio_phone_number):
    """
    Parameters
    ----------
    twilio_phone_number
        Twilio phone number string

    Returns
    -------
    Phone number portion of a Twilio phone number in the format -
    <channel>:<e164 formatted phone number>
    """
    return twilio_phone_number.split(':')[-1]

def save_message(request):
    """Saves incoming Twilio message from a HTTP request.

    Parameters
    ----------
    request
        Incoming message HTTP request

    Returns
    -------
    (message, is_from_new, is_to_new)
        message - Message model reference
        is_from_new - True if 'from user' was created new
        is_to_new - True if 'to user' was created new
    """
    # Create TwilioInboundMessage model
    message = models.TwilioInboundMessage(
        # Request Parameters
        api_version=request.data.get('ApiVersion'),
        message_sid=request.data.get('MessageSid'),
        sms_sid=request.data.get('SmsSid'),
        sms_message_sid=request.data.get('SmsMessageSid'),
        sms_status = request.data.get('SmsStatus'),
        account_sid=request.data.get('AccountSid'),
        from_str=request.data.get('From'),
        to_str=request.data.get('To'),
        body=request.data.get('Body'),
        num_media=request.data.get('NumMedia'),
        num_segments=request.data.get('NumSegments'),

        # Geographic Data-related Parameters
        from_city=request.data.get('FromCity'),
        from_state=request.data.get('FromState'),
        from_zip=request.data.get('FromZip'),
        from_country=request.data.get('FromCountry'),
        to_city=request.data.get('ToCity'),
        to_state=request.data.get('ToState'),
        to_zip=request.data.get('ToZip'),
        to_country=request.data.get('ToCountry'),

        # WhatsApp-specific Parameters
        profile_name=request.data.get('ProfileName'),
        wa_id=request.data.get('WaId'),
        forwarded=request.data.get('Forwarded'),
        frequently_forwarded=request.data.get('FrequentlyForwarded'),

        # WhatsApp Location Sharing Parameters
        latitude=request.data.get('Latitude'),
        longitude=request.data.get('Longitude'),
        address=request.data.get('Address'),
        label=request.data.get('Label')
    )

    # Commit message so we may create users associated with it
    message.save()

    # Get users and phone numbers

    from_raw_number = get_phone_number_string(message.from_str)
    (from_phone_number, from_ph_is_new) = get_phone_number(from_raw_number)
    (from_user, from_usr_is_new) = get_user(from_phone_number)

    to_raw_number = get_phone_number_string(message.to_str)
    (to_phone_number, to_ph_is_new) = get_phone_number(to_raw_number)
    (to_user, to_usr_is_new) = get_user(to_phone_number)

    # Update message with users and phone numbers

    message.from_user = from_user
    message.to_user = to_user

    message.from_phone_number = from_phone_number
    message.to_phone_number = to_phone_number

    message.save()

    return (message, from_ph_is_new, from_usr_is_new, to_ph_is_new,\
        to_usr_is_new)

def save_message_medias(request, message):
    """Save media associated with message.

    Parameters
    ----------
    request : HttpRequest
        HTTP request with full Twilio incoming message and medias
    message : TwilioInboundMessage
        Reference to message model row for which we're saving medias for
    """
    if message.num_media.isnumeric():
        for i in range(int(message.num_media)):
            # Create TwilioInboundMessageMedia model
            media = models.TwilioInboundMessageMedia(
                content_type = request.data[f'MediaContentType{i}'],
                url = request.data[f'MediaUrl{i}'],
                message=message
            )
            media.save()

def save_message_log(request, message):
    """Saves Twilio incoming message as a new log model row from a HTTP request.

    Parameters
    ----------
    request : HttpRequest
        Incoming message HTTP request
    message : TwilioInboundMessage
        Message to log
    """
    try:
        log_payload = 'request.stream\n'
        log_payload += str(request.stream) + '\n\n'
        log_payload += 'request.content_type\n'
        log_payload += str(request.content_type) + '\n\n'
        log_payload += 'request.method\n'
        log_payload += str(request.method) + '\n\n'
        log_payload += 'request.query_params\n'
        log_payload += str(request.query_params) + '\n\n'
        log_payload += 'request.headers\n'
        log_payload += str(request.headers) + '\n\n'
        log_payload += 'request.data\n'
        log_payload += str(dict(request.data))
        log_message = models.TwilioInboundMessageLogEntry(
            payload=log_payload,
            message=message
        )
        log_message.save()
        return True
    except:
        return False