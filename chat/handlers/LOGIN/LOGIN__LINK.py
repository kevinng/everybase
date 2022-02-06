import datetime
import pytz, datetime
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.render_message import render_message
from chat.handlers.library import MessageHandler
from relationships import models

class Handler(MessageHandler):
    def run(self):
        if self.message.body.strip().lower() == 'yes':
            # Only the latest token is used
            token = models.LoginToken.objects.filter(
                user=self.message.from_user.id,
                activated__isnull=True # Token not activated
            ).order_by('-created').first()

            if token is not None:
                sgtz = pytz.timezone(settings.TIME_ZONE)
                now = datetime.datetime.now(tz=sgtz)
                token.activated = now
                token.save()

                return self.done_reply(
                    intents.LOGIN,
                    messages.LOGIN__CONFIRMED)

            return self.done_reply(
                intents.LOGIN,
                messages.LOGIN__AGAIN)
            
        return render_message(messages.LOGIN__DO_NOT_UNDERSTAND, None)