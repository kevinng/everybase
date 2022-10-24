from chat import models

def save_message_medias(request, message):
    """Save media associated with message.

    Parameters
    ----------
    request : HttpRequest
        HTTP request with full Twilio incoming message and medias
    message : TwilioInboundMessage
        Reference to message model we're associating the medias with
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