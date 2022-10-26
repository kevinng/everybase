import pytz, datetime
from everybase.settings import TIME_ZONE
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from amplitude.constants import events
from relationships.models import Email
from chat.libraries.constants import datas
from chat.libraries.classes.message_handler import MessageHandler

class RegisterEmailHandler(MessageHandler):
    def run(self, intent_key, message_key, params_func=None):
        user = self.message.from_user
        body = self.message.body.strip().lower()

        try:
            try:
                email = Email.objects.get(email=body)
            except Email.DoesNotExist:
                email = Email(email=body)
                email.full_clean()
                email.save()

            user.email = email

            # This is the last step of registration - register user
            sgtz = pytz.timezone(TIME_ZONE)
            user.registered = datetime.datetime.now(tz=sgtz)

            user.save()
        except ValidationError:
            self.save_body_as_string(datas.STRAY_INPUT)
            self.send_event(events.ENTERED_STRAY_TEXT)
            return self.reply_invalid_email()
        except IntegrityError:
            self.save_body_as_string(datas.STRAY_INPUT)
            self.send_event(events.ENTERED_STRAY_TEXT)
            return self.reply_invalid_email()

        self.send_event(events.ENTERED_FREE_TEXT)
        
        return self.done_reply(
            intent_key,
            message_key,
            params_func=params_func
        )