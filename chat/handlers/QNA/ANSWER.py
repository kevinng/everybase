from relationships import models as relmods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def _get_match_id(self):
        if not hasattr(self, '_match_id') or self._match_id is None:
            # Lazy-instantiate, once-only
            self._match_id = self.get_latest_value(
                intents.QNA,
                messages.YOUR_QUESTION,
                datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
                False
            ).value_id
        
        return self._match_id

    def _get_buying_boolean(self):
        match = relmods.Match.objects.get(pk=self._get_match_id())
        if match.supply.user == self.message.from_user:
            # User is seller
            return False
        elif match.demand.user == self.message.from_user:
            # User is buyer
            return True
        return None

    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            QNA__ANSWER__INPUT__STRING)
        return self.done_reply(
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            { 'buying': self._get_buying_boolean() }
        )