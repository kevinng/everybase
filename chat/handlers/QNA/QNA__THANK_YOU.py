from amplitude.constants import events
from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.STRAY_INPUT)

        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            self.send_event(events.ENTERED_STRAY_TEXT)
            return self.done_reply(intents.MENU, messages.MENU)

        self.add_option([('1', 0)],
            intents.QNA,
            messages.QUESTION,
            datas.QNA,
            datas.QNA__ASK_QUESTION,
            amp_event_key=events.CHOSE_ASK_QUESTION_WITH_REPLY
        )
        self.add_option([('2', 0)],
            intents.QNA,
            messages.PLEASE_PAY,
            datas.QNA,
            datas.QNA__BUY_CONTACT,
            amp_event_key=events.CHOSE_BUY_CONTACT_WITH_REPLY
        )

        return self.reply_option()