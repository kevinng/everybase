import pytz, datetime
from everybase.settings import TIME_ZONE
from amplitude.constants import events
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class DiscussConfirmDetailsHandler(MessageHandler):
    def run(self):
        logic = ContextLogic(self)
        def get_no_message_key():
            if logic.is_buying():
                return messages.DEMAND__GET_PRODUCT
            else:
                return messages.SUPPLY__GET_PRODUCT

        def update_match(message_handler, data_value):
            """Updates match parameters after the user has chosen an option"""
            logic = ContextLogic(message_handler)
            sgtz = pytz.timezone(TIME_ZONE)
            match = logic.get_match()
            correct = data_value.value_string == datas.CONFIRM_DETAILS__YES
            
            # Update match
            if logic.is_buying():
                match.buyer_confirmed_details = datetime.datetime.now(sgtz)
                match.buyer_confirmed_details_correct = correct
                match.buyer_confirmed_details_correct_value = data_value
            else:
                match.seller_confirmed_details = datetime.datetime.now(sgtz)
                match.seller_confirmed_details_correct = correct
                match.seller_confirmed_details_correct_value = data_value
            match.save()

        self.add_option([('1', 0), ('yes', 0)],
            self.intent_key,
            messages.DISCUSS__ASK,
            datas.CONFIRM_DETAILS,
            datas.CONFIRM_DETAILS__YES,
            chosen_func=update_match,
            amp_event_key=events.CHOSE_YES_WITH_REPLY
        )
        self.add_option([('2', 0), ('no', 0)],
            intent_key=self.intent_key,
            message_key_func=get_no_message_key,
            data_key=datas.CONFIRM_DETAILS,
            data_value=datas.CONFIRM_DETAILS__NO,
            chosen_func=update_match,
            amp_event_key=events.CHOSE_NO_WITH_REPLY
        )

        return self.reply_option()