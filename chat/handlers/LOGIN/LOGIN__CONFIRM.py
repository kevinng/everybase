import datetime
import pytz, datetime
from django.urls import reverse
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.render_message import render_message
from chat.handlers.library import MessageHandler
from relationships import models
from relationships.utilities.kill_login_tokens import kill_login_tokens

class Handler(MessageHandler):
    def run(self):
        if self.message.body.strip().lower() == 'yes':
            # Use latest token
            token = models.LoginToken.objects.filter(
                user=self.message.from_user.id).order_by('-created').first()

            if token is not None and token.activated is None:
                # Activate token
                sgtz = pytz.timezone(settings.TIME_ZONE)
                now = datetime.datetime.now(tz=sgtz)
                token.activated = now
                token.save()

                # Kill other tokens
                kill_login_tokens(self.message.from_user, token.id)

                def params_func():
                    return {
                        'base_url': settings.BASE_URL,
                        'lead_create': reverse('leads:lead_create'),
                        'lead_list': reverse('leads:lead_list')
                    }

                return self.done_reply(
                    intents.LOGIN,
                    messages.LOGIN__CONFIRMED,
                    params_func=params_func
                )

            return self.done_reply(
                intents.LOGIN,
                messages.LOGIN__AGAIN)
            
        return render_message(messages.LOGIN__DO_NOT_UNDERSTAND, None)