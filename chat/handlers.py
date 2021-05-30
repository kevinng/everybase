"""This file defines all ContextHandler sub-classes - i.e., actual
implementation of what to do in each context.

Classes are named in the format:

<intent key>__<message key>
"""

from chat.libraries import (intents, messages, datas, model_utils)
from chat.libraries.message_handler import MessageHandler
from relationships import models as relmods

class SPEAK_HUMAN__CONFIRM_HUMAN(MessageHandler):
    def run(self):
        pass

class EXPLAIN_SERVICE__EXPLAIN_SERVICE(MessageHandler):
    def run(self):
        pass

# Menu intent

class MENU__MENU(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('buyers', 2)], intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT, {})
        self.add_option([('2', 0), ('sellers', 2)], intents.NEW_DEMAND, messages.DEMAND__GET_PRODUCT, {})
        self.add_option([('3', 0), ('human', 1)], intents.SPEAK_HUMAN, messages.CONFIRM_HUMAN, {})
        self.add_option([('4', 0), ('learn', 1)], intents.EXPLAIN_SERVICE, messages.EXPLAIN_SERVICE, {})
        return self.reply_option()

# REGISTER intent

class REGISTER__REGISTER__GET_NAME(MessageHandler):
    def run(self):
        # Store message body as user's name
        user = self.message.from_user
        user.name = self.message.body.strip()
        user.save()
        
        # Menu
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})

# DISCUSS_W_BUYER intent

class DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_TIMEFRAME(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE(MessageHandler):
    pass


# NEW_SUPPLY intent

class NEW_SUPPLY__SUPPLY__GET_PRODUCT(MessageHandler):
    def run(self):
        model_utils.save_body_as_string(
            self.message,
            self.intent_key,
            self.message_key,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )
        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY
        )

class NEW_SUPPLY__SUPPLY__GET_AVAILABILITY(MessageHandler):
    def run(self):
        pass

class NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE(MessageHandler):
    pass
    # def run(self):
    #     model_utils.save_body_as_string(
    #         self.message,
    #         self.intent_key,
    #         self.message_key,
    #         datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING
    #     )

    #     # Get product type
    #     value = model_utils.get_latest_value(
    #         intents.NEW_SUPPLY,
    #         messages.SUPPLY__GET_PRODUCT,
    #         datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
    #     )

    #     product_type = model_utils.get_product_type_with_match(value.value_string)

    #     if product_type is None:
    #         # We're not able to find a matching product type - ask for packing
    #         return self.done_reply(
    #             intents.NEW_SUPPLY,
    #             messages.SUPPLY__GET_PACKING
    #         )

    #     # We found a matching product type - confirm packing
    #     try:
    #         uom = relmods.UnitOfMeasure.objects.filter(
    #             product_type=product_type
    #         ).order_by('-priority').first()
    #         print(uom)
    #     except relmods.UnitOfMeasure.DoesNotExist:
    #         return self.done_reply(
    #             intents.NEW_SUPPLY,
    #             messages.SUPPLY__GET_PACKING
    #         )

    #     return self.done_reply(
    #         intents.NEW_SUPPLY,
    #         messages.SUPPLY__CONFIRM_PACKING,
    #         { 'packing_description': uom.description }
    #     )

class NEW_SUPPLY__SUPPLY__CONFIRM_PACKING(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_PACKING(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_QUANTITY(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_TIMEFRAME(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_PRICE(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_DEPOSIT(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__THANK_YOU(MessageHandler):
    pass


# NEW_DEMAND intent

class NEW_DEMAND__DEMAND__GET_PRODUCT(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__GET_COUNTRY_STATE(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__GET_QUANTITY(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__GET_PRICE(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__THANK_YOU(MessageHandler):
    pass


# DISCUSS_W_SELLER intent

class DISCUSS_W_SELLER__DEMAND__GET_PRODUCT(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_QUANTITY(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_PRICE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTERESTED(MessageHandler):
    pass

class DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM(MessageHandler):
    pass

class DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__CONFIRM_UPDATED(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__ASK(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED(MessageHandler):
    pass


# DISCUSS_W_BUYER intent

class DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTERESTED(MessageHandler):
    pass

class DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM(MessageHandler):
    pass

class DISCUSS_W_BUYER__STILL_INTERESTED__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__CONFIRM_UPDATED(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__ASK(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED(MessageHandler):
    pass


# STOP_DISCUSSION intent

class STOP_DISCUSSION__STOP_DISCUSSION__REASON(MessageHandler):
    pass

class STOP_DISCUSSION__STOP_DISCUSSION__THANK_YOU(MessageHandler):
    pass


# CONNECT intent

class CONNECT__PLEASE_PAY(MessageHandler):
    pass


# No intent

class NO_INTENT__YOUR_QUESTION(MessageHandler):
    pass

class NO_INTENT__YOUR_ANSWER(MessageHandler):
    pass

class NO_INTENT__PAYEE_CONNECTED(MessageHandler):
    pass

class NO_INTENT__NON_PAYEE_CONNECTED(MessageHandler):
    pass

class NO_INTENT__NO_MESSAGE(MessageHandler):
    def run(self):
        user = relmods.User.objects.get(pk=self.message.from_user.id)

        if user.name is None:
            # User's name not set - register
            return self.done_reply(
                intents.REGISTER, messages.REGISTER__GET_NAME)

        # No active context - menu
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})