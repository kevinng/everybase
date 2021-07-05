import pytz, datetime
from everybase.settings import TIME_ZONE
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class DiscussConfirmInterestHandler(MessageHandler):
    def run(self):
        logic = ContextLogic(self)
        if logic.get_match().closed is not None:
            # Match is closed - return menu
            return self.done_reply(intents.MENU, messages.MENU)

        def yes_message_key():
            """Returns message key if the user chooses yes"""
            if logic.is_connected():
                return messages.DISCUSS__ALREADY_CONNECTED
            else:
                return messages.DISCUSS__CONFIRM_DETAILS

        def update_match(message_handler, data_value):
            """Updates match parameters after the user has chosen an option"""
            logic = ContextLogic(message_handler)
            sgtz = pytz.timezone(TIME_ZONE)
            match = logic.get_match()
            interested = data_value.value_string == datas.CONFIRM_INTEREST__YES
            
            # Update match
            if logic.is_buying():
                match.buyer_confirmed_interest = datetime.datetime.now(sgtz)
                match.buyer_interested = interested
                match.buyer_confirmed_interest_value = data_value
            else:
                match.seller_confirmed_interest = datetime.datetime.now(sgtz)
                match.seller_interested = interested
                match.seller_confirmed_interest_value = data_value
            match.save()

        self.add_option([('1', 0), ('yes', 0)],
            self.intent_key,
            message_key_func=yes_message_key,
            data_key=datas.CONFIRM_INTEREST,
            data_value=datas.CONFIRM_INTEREST__YES,
            chosen_func=update_match
        )
        self.add_option([('2', 0), ('no', 0)],
            self.intent_key,
            messages.STILL_INTERESTED__CONFIRM,
            datas.CONFIRM_INTEREST,
            datas.CONFIRM_INTEREST__NO,
            chosen_func=update_match
        )

        return self.reply_option()