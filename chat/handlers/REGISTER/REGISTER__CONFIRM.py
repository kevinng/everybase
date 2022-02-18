import pytz
from datetime import datetime, timedelta
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.render_message import render_message
from chat.handlers.library import MessageHandler
from django.contrib.auth.models import User
from relationships import models
from relationships.utilities.kill_register_tokens import kill_register_tokens

class Handler(MessageHandler):
    def run(self):
        if self.message.body.strip().lower() == 'yes':
            # Create Django user
            # Note: Everybase user is automatically created for this number in
            # save_message.

            user = self.message.from_user
            django_user, _ = User.objects.get_or_create(
                username=user.uuid)

            # Set unusable password for Django user and save
            django_user.set_unusable_password()
            django_user.save()

            # Update user profile
            sgtz = pytz.timezone(settings.TIME_ZONE)
            user.registered = datetime.now(sgtz)
            user.django_user = django_user
            user.save()

            # Activate this token
            token = models.RegisterToken.objects.filter(user=user)\
                .order_by('-created').first()

            if token is not None:
                expiry_datetime = token.created + timedelta(
                seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
                sgtz = pytz.timezone(settings.TIME_ZONE)
                if datetime.now(tz=sgtz) < expiry_datetime and\
                    token.activated is None:
                    # Checks passed
                    #   Token is not expired
                    #   Token is not activated

                    # Activate token
                    sgtz = pytz.timezone(settings.TIME_ZONE)
                    now = datetime.now(tz=sgtz)
                    token.activated = now
                    token.save()
                else:
                    return self.done_reply(
                        intents.REGISTER,
                        messages.REGISTER__AGAIN
                    )

            # Kill all tokens
            kill_register_tokens(user)

            return self.done_reply(
                intents.REGISTER,
                messages.REGISTER__CONFIRMED)

        return render_message(messages.REGISTER__DO_NOT_UNDERSTAND, None)