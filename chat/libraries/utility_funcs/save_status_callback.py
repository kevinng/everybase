from chat import models

def save_status_callback(request, msg_id=None):
    """Save incoming Twilio status callback
    
    Parameters
    ----------
    request
        Incoming message HTTP request
    msg_id
        ID of outbound Twilio message to associate this callback with. If not
        none, will get message with this ID and associate it with this callback.
        Otherwise, will get message with this callback's Twilio message SID
        and assocate it with this callback.
    """
    message_sid = request.data.get('MessageSid')

    callback = models.TwilioStatusCallback(
        from_str=request.data.get('From'),
        to_str=request.data.get('To'),
        account_sid=request.data.get('AccountSid'),
        api_version=request.data.get('ApiVersion'),
        channel_install_sid=request.data.get('ChannelInstallSid'),
        channel_prefix=request.data.get('ChannelPrefix'),
        channel_status_code=request.data.get('ChannelStatusCode'),
        channel_status_message=request.data.get('ChannelStatusMessage'),
        channel_to_address=request.data.get('ChannelToAddress'),
        message_sid=message_sid,
        message_status=request.data.get('MessageStatus'),
        sms_sid=request.data.get('SmsSid'),
        sms_status=request.data.get('SmsStatus'),
        error_code=request.data.get('ErrorCode'),
        error_message=request.data.get('ErrorMessage'),
        event_type=request.data.get('EventType')
    )

    # Associate message
    try:
        if msg_id is None:
            message = models.TwilioOutboundMessage.objects.get(
                message_sid=message_sid)
        else:
            message = models.TwilioOutboundMessage.objects.get(pk=msg_id)
    except models.TwilioOutboundMessage.DoesNotExist:
        pass
    callback.message = message
    callback.save()

    return callback