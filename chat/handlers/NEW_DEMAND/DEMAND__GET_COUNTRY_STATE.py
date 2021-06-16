from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING)

        # Get TOP unit of measure for product type matching the latest data
        # value string of this user with the given keys. UOM is None if user's
        # input does not match any product type.
        _, uom = self.get_product_type(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is not None:
            # UOM found, confirm packing details
            return self.done_reply(
                intents.NEW_DEMAND,
                messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE,
                params={
                    'packing_description': uom.description,
                    'packing_plural': uom.plural_name
                }
            )
        else:
            # UOM not found, request packing details
            return self.done_reply(
                intents.NEW_DEMAND,
                messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
            )