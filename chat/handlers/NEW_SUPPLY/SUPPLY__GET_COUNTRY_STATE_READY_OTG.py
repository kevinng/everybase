from chat.libraries import intents, messages, datas
from chat.libraries.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
        NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING)

        # Get TOP unit of measure for product type matching the latest data
        # value string of this user with the given keys. UOM is None if user's
        # input does not match any product type.
        _, uom = self.get_product_type(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is not None:
            # UOM found, confirm packing details
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__CONFIRM_PACKING,
                params={ 'packing_description': uom.description }
            )
        else:
            # UOM not found, request packing details
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PACKING
            )