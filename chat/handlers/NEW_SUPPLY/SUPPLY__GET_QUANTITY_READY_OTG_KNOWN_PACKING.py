from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
    NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING)

        _, uom = self.get_product_type(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is None:
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING,
                None
            )

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING,
            { 'packing_singular' : uom.name }
        )