from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        quantity = self.save_body_as_string(datas.\
        NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__STRING)

        if quantity is None:
            # User input is invalid
            return self.reply_invalid_number()

        _, uom = self.get_product_type(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING
        )
        
        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE,
            { 'packing_single': uom.name }
        )