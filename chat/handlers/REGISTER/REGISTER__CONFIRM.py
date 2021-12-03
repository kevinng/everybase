import pytz, datetime
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.render_message import render_message
from chat.handlers.library import MessageHandler
from django.contrib.auth.models import User

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
            user.registered = datetime.datetime.now(sgtz)
            user.django_user = django_user
            user.save()

            return self.done_reply(
                intents.REGISTER,
                messages.REGISTER__CONFIRMED)

        return render_message(messages.REGISTER__DO_NOT_UNDERSTAND, None)