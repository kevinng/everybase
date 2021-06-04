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

# REGISTER intent

class REGISTER__REGISTER__GET_NAME(MessageHandler):
    def run(self):
        # Store message body as user's name
        user = self.message.from_user
        user.name = self.message.body.strip()
        user.save()
        
        # Menu
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})

# Menu intent

class MENU__MENU(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('buyers', 2)], intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT, {})
        self.add_option([('2', 0), ('sellers', 2)], intents.NEW_DEMAND, messages.DEMAND__GET_PRODUCT, {})
        self.add_option([('3', 0), ('human', 1)], intents.SPEAK_HUMAN, messages.CONFIRM_HUMAN, {})
        self.add_option([('4', 0), ('learn', 1)], intents.EXPLAIN_SERVICE, messages.EXPLAIN_SERVICE, {})
        return self.reply_option()

# DISCUSS_W_BUYER intent

class DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG(MessageHandler):
    def run(self):
        pass

class DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PRE_ORDER(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE_PRE_ORDER(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC(MessageHandler):
    pass

class DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM(MessageHandler):
    pass

class DISCUSS_W_BUYER__STILL_INTERESTED__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__ASK(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS(MessageHandler):
    pass

# NEW_SUPPLY intent

class NEW_SUPPLY__SUPPLY__GET_PRODUCT(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING)
        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY
        )

class NEW_SUPPLY__SUPPLY__GET_AVAILABILITY(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('otg', 0), ('ready', 1)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            {},
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )
        self.add_option([('2', 0), ('pre order', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            {},
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )
        return self.reply_option()

class GetCountryStateBaseHandler(MessageHandler):
    def _run(self):
        self.save_body_as_string(datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING)
        uom = model_utils.get_uom_with_product_type_keys(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is not None:
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__CONFIRM_PACKING,
                params={ 'packing_description': uom.description }
            )
        else:
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PACKING
            )

class NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG(GetCountryStateBaseHandler):
    def run(self):
        return self._run()

class NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER(GetCountryStateBaseHandler):
    def run(self):
        return self._run()

class NEW_SUPPLY__SUPPLY__CONFIRM_PACKING(MessageHandler):
    def run(self):
        availability = model_utils.get_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE
        ).value_string

        # The first option directs to a different message depending on what the
        # user enter for availability earlier on
        yes_intent = intents.NEW_SUPPLY
        if availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG:
            yes_message = messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        elif availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER:
            yes_message = messages.SUPPLY__GET_QUANTITY_PRE_ORDER

        self.add_option([('1', 0), ('yes', 0)], yes_intent, yes_message, {})
        self.add_option([('2', 0), ('no', 0)], intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING, {})
        return self.reply_option()

class NEW_SUPPLY__SUPPLY__GET_PACKING(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING)
        
        # Direct to the right message depending on what the user entered for
        # availability earlier on

        availability = model_utils.get_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE
        ).value_string

        if availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG:
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
            )
        elif availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER:
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_QUANTITY_PRE_ORDER
            )

class NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING)
        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )

class NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_QUANTITY_PRE_ORDER(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_PRICE_PRE_ORDER(MessageHandler):
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

class NEW_DEMAND__NEW_DEMAND__DEMAND__GET_QUANTITY(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class NEW_DEMAND__DEMAND__THANK_YOU(MessageHandler):
    pass


# DISCUSS_W_SELLER intent

class DISCUSS_W_SELLER__DEMAND__GET_PRODUCT(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST(MessageHandler):
    pass

class DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM(MessageHandler):
    pass

class DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__ASK(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__THANK_YOU(MessageHandler):
    pass

# Q&A intent

class QNA__YOUR_QUESTION(MessageHandler):
    pass

class QNA__YOUR_ANSWER(MessageHandler):
    pass

class QNA__ASK_QUESTION(MessageHandler):
    pass

class QNA__THANK_FOR_QUESTION(MessageHandler):
    pass

class QNA__REPLY(MessageHandler):
    pass

class QNA__THANK_FOR_REPLY(MessageHandler):
    pass

class QNA__STOP_DISCUSSION_REASON(MessageHandler):
    pass

class QNA__STOP_DISCUSSION__STOP_DISCUSSION__THANK_YOU(MessageHandler):
    pass

# CONNECT intent

class CONNECT__PLEASE_PAY(MessageHandler):
    pass

class CONNECT__CONNECTED(MessageHandler):
    pass

# No intent

class NO_INTENT__NO_MESSAGE(MessageHandler):
    def run(self):
        user = relmods.User.objects.get(pk=self.message.from_user.id)

        if user.name is None:
            # User's name not set - register
            return self.done_reply(
                intents.REGISTER, messages.REGISTER__GET_NAME)

        # No active context - menu
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})