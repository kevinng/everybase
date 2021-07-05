from chat import models
from chat.libraries.constants import messages
from chat.libraries.sub_classes.message_handlers.\
    discuss__confirm_details_handler import \
    DiscussConfirmDetailsHandler

class Handler(DiscussConfirmDetailsHandler):
    def __init__(self, message: models.TwilioInboundMessage, intent_key: str,
        message_key: str):
        super().__init__(message, intent_key, message_key)

        self._no_message_key = messages.SUPPLY__GET_AVAILABILITY