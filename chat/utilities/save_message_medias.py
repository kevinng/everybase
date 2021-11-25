from django.http.request import HttpRequest
from chat import models

def save_message_medias(
        request : HttpRequest,
        message : models.TwilioInboundMessage
    ):
    """Save media associated with message.

    Parameters
    ----------
    request
        HTTP request with full Twilio incoming message and medias.
    message
        Reference to message model we're associating the medias with.
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