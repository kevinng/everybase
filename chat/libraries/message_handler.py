from chat import models
from chat.libraries import (intents, messages, context_utils, model_utils, nlp)

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
        self.options = []

        self.dataset = self.get_dataset()

    def run(self):
        """Extract/validate/store data, return reply message body, and set new
        context.

        Override.
        """
        return None

    def add_option(self, match_strs, intent_key, message_key, params,
        data_key=None, data_value=None):
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
        data_key : string, optional
            If present, store user's input under context/data-key
        data_value : string, optional
            If present, store user's input under context/data-key with this value
        """
        self.options.append(
            (match_strs, intent_key, message_key, params, data_key, data_value))

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
        """Run nlp.match_each_token against each option in against message body.

        Set context and return message body of the FIRST matching option.

        If data key/value is/are provided for an option, store user's choice.

        If no matching option is found - return reply_invalid_option value.
        """
        for o in self.options:
            match_strs, intent_key, message_key, params, data_key, data_value = o
            for match_str, tolerance in match_strs:
                if nlp.match(self.message.body, match_str, tolerance):
                    if data_key is not None:
                        # Data key is specified - store user's choice
                        if data_value is not None:
                            # Data value is specified, use it as data value
                            value = data_value
                        else:
                            # Data value is not specified, use key as data value
                            value = data_key
                        self.save_value(data_key, value_string=value)
                    return self.done_reply(intent_key, message_key, params)

        return self.reply_invalid_option()

    def reply_invalid_option(self):
        """Default reply when the user sends an invalid option.
        """
        # Note: we don't need to set a new context. I.e. the user remains in
        # the current context.
        return messages.get_body(messages.DO_NOT_UNDERSTAND_OPTION, {})

    def reply_invalid_number(self):
        """Reply user entered an invalid number
        """
        # Note: we don't need to set a new context. I.e. the user remains in
        # the current context.
        return messages.get_body(messages.DO_NOT_UNDERSTAND_NUMBER, {})

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
        # Get current context
        now_intent_key, now_message_key = \
            context_utils.get_context(self.message.from_user)

        # Done current context
        context_utils.done_context(self.message.from_user, now_intent_key,
            now_message_key)

        # Start next context
        context_utils.start_context(self.message.from_user, intent_key,
            message_key)

    def get_dataset(self):
        """Get dataset for this message.
        """
        dataset, _ = models.MessageDataset.objects.get_or_create(
            intent_key=self.intent_key,
            message_key=self.message_key,
            in_message=self.message,
            user=self.message.from_user
        )

        return dataset

    def save_value(self, data_key, value_string=None, value_float=None,
        value_boolean=None, value_id=None):
        """Save data value in current context with specified data key

        Parameters
        ----------
        data_key : String
            Data key to save this value under
        value_string : String
            Set to value if value is of type string
        value_float : Float
            Set to value if value is of type float
        value_boolean : Boolean
            Set to value if value is of type boolean
        value_id : Integer
            Set to value if value is of type integer and is a model ID

        Returns
        -------
        Data value reference created
        """
        return models.MessageDataValue.objects.create(
            dataset=self.dataset,
            data_key=data_key,
            value_string=value_string,
            value_float=value_float,
            value_boolean=value_boolean,
            value_id=value_id
        )

    def save_body_as_string(self, data_key):
        """Save message body as data value string in current context

        Parameters
        ----------
        data_key : String
            Data key for the data value string
        """
        return self.save_value(data_key, value_string=self.message.body)

    def save_body_as_float(self, data_key):
        """Save message body in current context with specified data key as float

        Parameters
        ----------
        data_key
            Data key to store the message body against

        Returns
        -------
        Float value if successful, None if unable to convert body to float value
        """
        try:
            value = float(self.message.body.strip())
        except ValueError:
            return None

        return self.save_value(data_key, value_float=value)

    def get_uom_with_product_type_keys(self, intent_key, message_key, data_key):
        """Convenience method to call model_utils.get_uom_with_product_type_keys
        with this message's sender
        """
        return model_utils.get_uom_with_product_type_keys(
            intent_key,
            message_key,
            data_key,
            self.message.from_user
        )

    def get_latest_value(self, intent_key, message_key, data_key):
        return model_utils.get_latest_value(
            intent_key, message_key, data_key,
            self.message.from_user
        )