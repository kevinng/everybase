from amplitude.constants import events
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class SupplyConfirmPackingHandler(MessageHandler):
    def run(self):
        def yes_message_key():
            logic = ContextLogic(self)
            if logic.is_ready_otg():
                if logic.is_known_packing():
                    return messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
                else:
                    return messages.\
                        SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
            elif logic.is_pre_order():
                return messages.SUPPLY__GET_QUANTITY_PRE_ORDER

        self.add_option([('1', 0), ('yes', 0)],
            self.intent_key,
            message_key_func=yes_message_key,
            data_key=datas.CONFIRM_PACKING,
            data_value=datas.CONFIRM_PACKING__YES,
            amp_event_key=events.CHOSE_YES_WITH_REPLY
        )
        self.add_option([('2', 0), ('no', 0)],
            self.intent_key,
            messages.SUPPLY__GET_PACKING,
            datas.CONFIRM_PACKING,
            datas.CONFIRM_PACKING__NO,
            amp_event_key=events.CHOSE_NO_WITH_REPLY
        )

        return self.reply_option()