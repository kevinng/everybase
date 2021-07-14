from chat import models

def save_message_log(request, callback):
    """Log Twilio status callback and HTTP request.

    Parameters
    ----------
    request : HttpRequest
        Incoming message HTTP request
    callback : TwilioStatusCallback
        Callback to log
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
        
        models.TwilioStatusCallbackLogEntry.objects.create(
            payload=log_payload,
            callback=callback
        )
    except:
        return False

    return True