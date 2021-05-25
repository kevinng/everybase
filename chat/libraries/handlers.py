"""This file defines all ContextHandler sub-classes - i.e., actual
implementation of what to do in each context.

Classes are named in the format:

<intent key>__<message key>
"""

from chat import models

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

# REGISTER intent

class REGISTER__REGISTER__GET_NAME(MessageHandler):
    pass

class REGISTER__MENU(MessageHandler):
    pass

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
    pass

class NEW_SUPPLY__SUPPLY__GET_AVAILABILITY(MessageHandler):
    pass

class NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE(MessageHandler):
    pass

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

class NO_INTENT__MENU(MessageHandler):
    pass

class NO_INTENT__DO_NOT_UNDERSTAND(MessageHandler):
    pass

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
        # Check if user has name, if not - register him

        
        pass