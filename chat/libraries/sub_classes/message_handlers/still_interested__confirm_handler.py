import pytz, datetime
from everybase.settings import TIME_ZONE
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class StillInterestedConfirmHandler(MessageHandler):
    def run(self):
        def update_match(message_handler, data_value):
            """Updates match parameters after the user has chosen an option"""
            logic = ContextLogic(message_handler)
            sgtz = pytz.timezone(TIME_ZONE)
            match = logic.get_match()
            interested = data_value.value_string == datas.STILL_INTERESTED__YES
            
            # Update match
            buying = logic.is_buying()
            if buying == True:
                match.buyer_confirmed_still_interested = \
                    datetime.datetime.now(sgtz)
                match.buyer_still_interested = interested
                match.buyer_still_interested_value = data_value
            elif buying == False:
                match.seller_confirmed_still_interested = \
                    datetime.datetime.now(sgtz)
                match.seller_still_interested = interested
                match.seller_still_interested_value = data_value
            match.save()

        self.add_option([('1', 0), ('yes', 0)],
            self.intent_key,
            messages.STILL_INTERESTED__THANK_YOU,
            datas.STILL_INTERESTED,
            datas.STILL_INTERESTED__YES,
            chosen_func=update_match
        )
        self.add_option([('2', 0), ('no', 0)],
            self.intent_key,
            messages.STILL_INTERESTED__THANK_YOU,
            datas.STILL_INTERESTED,
            datas.STILL_INTERESTED__NO,
            chosen_func=update_match
        )

        return self.reply_option()