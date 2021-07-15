from relationships import models as relmods
from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.get_chatbot_phone_number import \
    get_chatbot_phone_number

def run():
    send_message(
        'Hello world',
        get_chatbot_phone_number(),
        relmods.User.objects.get(pk=4).phone_number,
        intent_key=intents.NO_INTENT,
        message_key=messages.NO_MESSAGE
    )