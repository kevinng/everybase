from everybase import settings
from relationships import models as relmods
from chat import models
from chat.constants import intents, messages
from chat.utilities import send_message

def run():
    send_message(
        'Hello world',
        models.User.objects.get(pk=settings.CHATBOT_USER_PK),
        relmods.User.objects.get(pk=4).phone_number,
        intent_key=intents.NO_INTENT,
        message_key=messages.NO_MESSAGE
    )