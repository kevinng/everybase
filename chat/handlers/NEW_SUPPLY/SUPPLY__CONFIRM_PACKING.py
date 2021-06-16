from chat.libraries import intents, messages, datas
from chat.libraries.message_handler import MessageHandler

class Handler(MessageHandler):
    def _get_yes_message_key(self):
        # Get latest availability choice entered by user in context
        availability = self.get_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE
        ).value_string

        if availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG:
            # Goods are ready/OTG, get quantity of known packing

            _, uom = self.get_product_type(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PRODUCT,
                datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
            )

            if uom is not None:
                # Product type and packing is known
                return messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
            else:
                # Product type and packing is not known
                return messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING

        elif availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER:
            # Goods are pre-order, get quantity and timeframe
            return messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        
        return None

    def _get_yes_params(self):
        _, uom = self.get_product_type(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is None:
            return {}

        return {
            'packing_plural' : uom.plural_name
        }

    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.NEW_SUPPLY, 
            None,
            self._get_yes_params,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES,
            None,
            self._get_yes_message_key
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PACKING,
            None,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO
        )
        return self.reply_option()