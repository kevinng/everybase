"""Mapping of context to handler"""

from chat.libraries import intents, messages, handlers

handler_context_map = {
    intents.SPEAK_HUMAN: {
        messages.CONFIRM_HUMAN: handlers.SPEAK_HUMAN__CONFIRM_HUMAN
    },
    intents.EXPLAIN_SERVICE: {
        messages.EXPLAIN_SERVICE: handlers.EXPLAIN_SERVICE__EXPLAIN_SERVICE
    },
    intents.REGISTER: {
        messages.REGISTER__GET_NAME: handlers.REGISTER__REGISTER__GET_NAME # DONE
    },
    intents.MENU: {
        messages.MENU: handlers.MENU__MENU
    },
    intents.NEW_SUPPLY: {
        messages.SUPPLY__GET_PRODUCT: handlers.NEW_SUPPLY__SUPPLY__GET_PRODUCT,
        messages.SUPPLY__GET_AVAILABILITY: handlers.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY,
        messages.SUPPLY__GET_COUNTRY_STATE: handlers.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE,
        messages.SUPPLY__CONFIRM_PACKING: handlers.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING,
        messages.SUPPLY__GET_PACKING: handlers.NEW_SUPPLY__SUPPLY__GET_PACKING,
        messages.SUPPLY__GET_QUANTITY: handlers.NEW_SUPPLY__SUPPLY__GET_QUANTITY,
        messages.SUPPLY__GET_TIMEFRAME: handlers.NEW_SUPPLY__SUPPLY__GET_TIMEFRAME,
        messages.SUPPLY__GET_PRICE: handlers.NEW_SUPPLY__SUPPLY__GET_PRICE,
        messages.SUPPLY__GET_DEPOSIT: handlers.NEW_SUPPLY__SUPPLY__GET_DEPOSIT,
        messages.SUPPLY__GET_ACCEPT_LC: handlers.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC,
        messages.SUPPLY__THANK_YOU: handlers.NEW_SUPPLY__SUPPLY__THANK_YOU
    },
    intents.NEW_DEMAND: {
        messages.DEMAND__GET_PRODUCT: handlers.NEW_DEMAND__DEMAND__GET_PRODUCT,
        messages.DEMAND__GET_COUNTRY_STATE: handlers.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE,
        messages.DEMAND__GET_QUANTITY: handlers.NEW_DEMAND__DEMAND__GET_QUANTITY,
        messages.DEMAND__GET_PRICE: handlers.NEW_DEMAND__DEMAND__GET_PRICE,
        messages.DEMAND__THANK_YOU: handlers.NEW_DEMAND__DEMAND__THANK_YOU
    },
    intents.DISCUSS_W_BUYER: {
        messages.SUPPLY__GET_PRODUCT: handlers.DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT,
        messages.SUPPLY__GET_AVAILABILITY: handlers.DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY,
        messages.SUPPLY__GET_COUNTRY_STATE: handlers.DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE,
        messages.SUPPLY__CONFIRM_PACKING: handlers.DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING,
        messages.SUPPLY__GET_PACKING: handlers.DISCUSS_W_BUYER__SUPPLY__GET_PACKING,
        messages.SUPPLY__GET_QUANTITY: handlers.DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY,
        messages.SUPPLY__GET_TIMEFRAME: handlers.DISCUSS_W_BUYER__SUPPLY__GET_TIMEFRAME,
        messages.SUPPLY__GET_PRICE: handlers.DISCUSS_W_BUYER__SUPPLY__GET_PRICE,
        messages.SUPPLY__GET_DEPOSIT: handlers.DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT,
        messages.SUPPLY__GET_ACCEPT_LC: handlers.DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC,
        messages.DISCUSS__CONFIRM_INTERESTED: handlers.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTERESTED,
        messages.STILL_INTERESTED__CONFIRM: handlers.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM,
        messages.STILL_INTERESTED__THANK_YOU: handlers.DISCUSS_W_BUYER__STILL_INTERESTED__THANK_YOU,
        messages.DISCUSS__CONFIRM_UPDATED: handlers.DISCUSS_W_BUYER__DISCUSS__CONFIRM_UPDATED,
        messages.DISCUSS__ASK: handlers.DISCUSS_W_BUYER__DISCUSS__ASK,
        messages.DISCUSS__THANK_YOU: handlers.DISCUSS_W_BUYER__DISCUSS__THANK_YOU,
        messages.ALREADY_CONNECTED: handlers.DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED
    },
    intents.DISCUSS_W_SELLER: {
        messages.DEMAND__GET_PRODUCT: handlers.DISCUSS_W_SELLER__DEMAND__GET_PRODUCT,
        messages.DEMAND__GET_COUNTRY_STATE: handlers.DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE,
        messages.DEMAND__GET_QUANTITY: handlers.DISCUSS_W_SELLER__DEMAND__GET_QUANTITY,
        messages.DEMAND__GET_PRICE: handlers.DISCUSS_W_SELLER__DEMAND__GET_PRICE,
        messages.DISCUSS__CONFIRM_INTERESTED: handlers.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTERESTED,
        messages.STILL_INTERESTED__CONFIRM: handlers.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM,
        messages.STILL_INTERESTED__THANK_YOU: handlers.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU,
        messages.DISCUSS__CONFIRM_UPDATED: handlers.DISCUSS_W_SELLER__DISCUSS__CONFIRM_UPDATED,
        messages.DISCUSS__ASK: handlers.DISCUSS_W_SELLER__DISCUSS__ASK,
        messages.DISCUSS__THANK_YOU: handlers.DISCUSS_W_SELLER__DISCUSS__THANK_YOU,
        messages.ALREADY_CONNECTED: handlers.DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED
    },
    intents.STOP_DISCUSSION: {
        messages.STOP_DISCUSSION__REASON: handlers.STOP_DISCUSSION__STOP_DISCUSSION__REASON,
        messages.STOP_DISCUSSION__THANK_YOU: handlers.STOP_DISCUSSION__STOP_DISCUSSION__THANK_YOU
    },
    intents.CONNECT: {
        messages.PLEASE_PAY: handlers.CONNECT__PLEASE_PAY,
    },
    intents.NO_INTENT: {
        messages.YOUR_QUESTION: handlers.NO_INTENT__YOUR_QUESTION,
        messages.YOUR_ANSWER: handlers.NO_INTENT__YOUR_ANSWER,
        messages.PAYEE_CONNECTED: handlers.NO_INTENT__PAYEE_CONNECTED,
        messages.NON_PAYEE_CONNECTED: handlers.NO_INTENT__NON_PAYEE_CONNECTED,
        messages.NO_MESSAGE: handlers.NO_INTENT__NO_MESSAGE # DONE
    }
}

def get_handler(message, intent_key, message_key):
    """Get handler for message and context (i.e., intent_key, message_key).

    Parameters
    ----------
    message : TwilioInboundMessage
        Message for which we're getting a MessageHandler for
    intent_key : str
        Intent key
    message_key : str
        Message key

    Returns
    -------
    MessageHandler for message
    """
    return handler_context_map[intent_key]\
        [message_key](message, intent_key, message_key)