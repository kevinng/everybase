from amplitude.constants import events
from chat.tasks.save_lead_media import save_lead_media
from chat.libraries.constants import messages
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.classes.context_logic import ContextLogic
from relationships.models import LeadText

class GetLeadDetailsHandler(MessageHandler):
    def run(self):
        user = self.message.from_user
        lead = user.current_lead
        for m in self.message.medias.all():
            save_lead_media.delay(lead.id, m.content_type, m.url)

        if self.message.body.strip().lower() == 'done':
            def none_current_lead():
                user.current_lead = None

            c = ContextLogic(self)
            return self.done_reply(
                self.intent_key,
                messages.GET_LEAD__THANK_YOU,
                params_func=lambda : {
                    'is_buying': c.is_buying__current_lead()
                },
                done_func=none_current_lead
            )
        else:
            LeadText.objects.create(
                lead=lead,
                text=self.message.body.strip()
            )

        self.send_event(events.ENTERED_FREE_TEXT)

        return render_message(messages.GET_LEAD__DETAILS_PROMPT, None)