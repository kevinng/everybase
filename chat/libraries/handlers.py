"""This file defines all ContextHandler sub-classes - i.e., actual
implementation of what to do in each context.

Classes are named in the format:

<intent key>__<message key>
"""

from datetime import datetime
from everybase import settings
import pytz
from chat import models
from chat.libraries import (context_utils, intents, messages, datas,
    model_utils, nlp)
from relationships import models as relmods

class MessageHandler:
    """A context is a unique pair of the user's intent, and the last message
    sent by the system. A user's context may be ascertained by reading the
    intent_key and message_key of the last outbound Twilio message sent by the
    system.

    A message handler lets us handle an incoming message using the message-
    handling cycle:
        - Receive message.
        - Get user's intent and our last outbound message (i.e., context)
        - Extract data from message based on the context. Each context has its
            method to extract/store data from the incoming message.
        - Validate extracted data based on the context. Each context has its
            method to validate extracted data and store the results.
        - If the data is invalid - reply 'do-not-understand'.
        - If the data is valid - process input, ascertain/set next context,
            reply with right message.

    Attributes
    ----------
    message : TwilioInboundMessage
        Twilio inbound message we're handling
    """
    message = None
    dataset = None

    # Context
    intent_key = None
    message_key = None

    options = []

    def __init__(self, message, intent_key, message_key):
        """
        Parameters
        ----------
        message : TwilioInboundMessage
            Twilio inbound message we're handling
        """
        if message == None:
            raise Exception('message cannot be null')

        self.message = message
        self.intent_key = intent_key
        self.message_key = message_key

        self.get_or_create_dataset()

    def run(self):
        """Extract/validate/store data, return reply message body, and set new
        context.

        Override.
        """
        return None

    def add_option(self, match_strs, intent_key, message_key, params):
        """Add an option to this handler to be matched against the message body.
        To be used with the reply_option method.

        Options should be added in order of priority - i.e., more important
        added first.

        Parameters
        ----------
        match_strs : list of tuples
            List of strings to match for this option in the format:
            
            [(string_to_match, edit_distance_tolerance), ...]
            
            A string will be matched against the text body with the
            nlp.match_each_token function.
        intent_key : string
            Intent key for the context to set if this option is chosen
        message_key : string
            Message key for the context to set if this option is chosen
        params : dictionary
            Params to merge into the message body for this option
        """
        self.options.append((match_strs, intent_key, message_key, params))

    def done_reply(self, intent_key, message_key, params={}):
        """Convenience function to call self.done_to_context and
        messages.get_body in 1 function.

        Parameters
        ----------
        intent_key : string
            Intent key for the context to set
        message_key : string
            Message key for the context to set and message body to return
        """
        self.done_to_context(intent_key, message_key)
        return messages.get_body(message_key, params)

    def reply_option(self):
        """Run nlp.match_each_token against each option in this handler against
        the message body.

        Set context and return message body of the first matching option.

        If no matching option is found - return reply_invalid_option value.
        """
        tokens = self.message.body.split()
        for o in self.options:
            for t in o[0]:
                match_str = t[0]
                tolerance = t[1]
                if nlp.match_each_token(tokens, match_str, tolerance):
                    intent_key = o[1]
                    message_key = o[2]
                    params = o[3]
                    return self.done_reply(intent_key, message_key, params)

        return self.reply_invalid_option()

    def reply_invalid_option(self):
        """Default reply when the user sends an invalid option.
        """
        # Note: we don't need to set a new context
        return messages.get_body(messages.DO_NOT_UNDERSTAND, {})

    def done_to_context(self, intent_key, message_key):
        """Switch from the current context to the specified context. Set current
        context's done time to now.

        Parameters
        ----------
        intent_key : string
            Intent key as defined in intents.py for next context
        message_key : string
            Message key as defined in messages.py for next context
        """
        # Done current context
        now_intent_key, now_message_key = \
            context_utils.get_context(self.message.from_user)

        if now_message_key != messages.NO_MESSAGE and \
            now_intent_key != intents.NO_INTENT:
            # Only update current context if they're not 'no intent' and
            # 'no message'
            context_utils.done_context(self.message.from_user, now_intent_key,
                now_message_key)

        # Start next context
        context_utils.start_context(self.message.from_user, intent_key,
            message_key)
        
    def pause_to_context(self, intent_key, message_key):
        """Switch from the current context to the specified context. Set current
        context's paused time to now.

        Parameters
        ----------
        intent_key : string
            Intent key as defined in intents.py
        message_key : string
            Message key as defined in messages.py
        """
        # Pause current context
        now_intent_key, now_message_key = \
            context_utils.get_context(self.message.from_user)
        if now_message_key != messages.NO_MESSAGE and \
            now_intent_key != intents.NO_INTENT:
            context_utils.pause_context(self.message.from_user, now_intent_key,
                now_message_key)

        # Start next context
        context_utils.start_context(self.message.from_user, intent_key,
            message_key)

    def expire_to_context(self, intent_key, message_key):
        """Switch from the current context to the specified context. Set current
        context's expired time to now.

        Parameters
        ----------
        intent_key : string
            Intent key as defined in intents.py
        message_key : string
            Message key as defined in messages.py
        """
        # Expire current context
        now_intent_key, now_message_key = \
            context_utils.get_context(self.message.from_user)
        if now_message_key != messages.NO_MESSAGE and \
            now_intent_key != intents.NO_INTENT:
            context_utils.expire_context(self.message.from_user, now_intent_key,
                now_message_key)

        # Start next context
        context_utils.start_context(self.message.from_user, intent_key,
            message_key)

    def get_or_create_dataset(self):
        """Read/create dataset for this message.

        Do not override.
        """
        self.dataset, _ = models.MessageDataset.objects.get_or_create(
            message=self.message,
            intent_key=self.intent_key,
            message_key=self.message_key
        )

    def save_string(self, value, is_valid):
        """Save extracted string for this message/context.

        Do not override.
        """
        models.MessageDataString.objects.create(
            dataset=self.dataset,
            value=value,
            is_valid=is_valid
        )

    def save_float(self, value, is_valid):
        """Save extracted float for this message/context.

        Do not override.
        """
        models.MessageDataFloat.objects.create(
            dataset=self.dataset,
            value=value,
            is_valid=is_valid
        )

    def save_boolean(self, value, is_valid):
        """Save extracted boolean for this message/context.

        Do not override.
        """
        models.MessageDataBoolean.objects.create(
            dataset=self.dataset,
            value=value,
            is_valid=is_valid
        )

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