from amplitude.constants import events
from chat.libraries.constants import messages
from chat.libraries.classes.message_handler import MessageHandler
from relationships.models import Lead, CAPTURE_METHOD_TYPE__MENU_OPTION

class GetLeadLocationHandler(MessageHandler):
    def run(self, buying):
        user = self.message.from_user
        lead = Lead.objects.create(
            owner=user,
            capture_method_type=CAPTURE_METHOD_TYPE__MENU_OPTION,
            is_buying=buying,
            location=self.message.body.strip() # Store location
        )
        user.current_lead = lead
        user.save()
        self.send_event(events.ENTERED_FREE_TEXT)
        return self.done_reply(
            self.intent_key,
            messages.GET_LEAD__DETAILS,
            params_func=lambda : { 'buying': buying }
        )