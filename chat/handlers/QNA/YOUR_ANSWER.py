from relationships import models as relmods
from payments import models as paymods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.utilities.get_payment_link import get_payment_link

class Handler(MessageHandler):
    def _get_match_id(self):
        if not hasattr(self, '_match_id') or self._match_id is None:
            # Lazy-instantiate, once-only
            self._match_id = self.get_latest_value(
                intents.QNA,
                messages.YOUR_ANSWER,
                datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
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

    def _get_ask_question_params(self):
        return { 'buying': self._get_buying_boolean() }

    def _get_please_pay_params(self):
        hash = paymods.PaymentHash.objects.get(match=self._get_match_id())
        return {
            'buying': self._get_buying_boolean(),
            'currency': hash.currency.name,
            'price': hash.unit_amount,
            'payment_link': get_payment_link(hash.id)
        }

    def _get_stop_discussion__reason_params(self):
        return { 'buying': self._get_buying_boolean() }

    def run(self):
        match = relmods.Match.objects.get(pk=self._get_match_id())
        if match.closed is not None:
            # Match is closed for discussion - return menu
            user = relmods.User.objects.get(pk=self.message.from_user.id)
            return self.done_reply(
                intents.MENU,
                messages.MENU,
                {'name': user.name}
            )

        self.add_option([('1', 0)],
            intents.QNA,
            messages.QUESTION,
            self._get_ask_question_params,
            datas.QNA__YOUR_ANSWER__OPTION__CHOICE,
            datas.QNA__YOUR_ANSWER__OPTION__ASK_QUESTION
        )
        self.add_option([('2', 0)],
            intents.CONNECT,
            messages.PLEASE_PAY,
            self._get_please_pay_params,
            datas.QNA__YOUR_ANSWER__OPTION__CHOICE,
            datas.QNA__YOUR_ANSWER__OPTION__BUY_CONTACT
        )
        self.add_option([('3', 0)],
            intents.QNA,
            messages.STOP_DISCUSSION__REASON,
            self._get_stop_discussion__reason_params,
            datas.QNA__YOUR_ANSWER__OPTION__CHOICE,
            datas.QNA__YOUR_ANSWER__OPTION__STOP_DISCUSSION
        )
        return self.reply_option()