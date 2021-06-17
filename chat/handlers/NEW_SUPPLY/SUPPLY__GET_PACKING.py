from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING)
        
        # Get latest availability choice entered by user in context
        availability = self.get_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE
        ).value_string

        if availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG:
            # Goods are ready/OTG, get quantity of unknown packing

            product_type, uom = self.get_product_type(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PRODUCT,
                datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
            )

            if product_type is None:
                return self.done_reply(
                    intents.NEW_SUPPLY,
                    messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
                )
            else:
                return self.done_reply(
                    intents.NEW_SUPPLY,
                    messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING,
                    { 'packing_plural': uom.plural_name }
                )
        elif availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER:
            # Goods are pre-order, get quantity and timeframe
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_QUANTITY_PRE_ORDER
            )