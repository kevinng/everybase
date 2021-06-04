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

        self.get_or_create_dataset()

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
        """Run nlp.match_each_token against each option in this handler against
        the message body.

        Set context and return message body of the first matching option.

        If optional data key/value is/are provided for an option, store them
        when the user selects that option.

        If no matching option is found - return reply_invalid_option value.
        """
        for o in self.options:
            for t in o[0]:
                match_str = t[0]
                tolerance = t[1]
                if nlp.match(self.message.body, match_str, tolerance):
                    intent_key = o[1]
                    message_key = o[2]
                    params = o[3]
                    data_key = o[4]
                    data_value = o[5]
                    if data_key is not None:
                        if data_value is not None:
                            value = data_value
                        else:
                            value = data_key
                        # Store user's choice
                        dataset, _ = models.MessageDataset.objects.get_or_create(
                            # Note: store current context not incoming context
                            intent_key=self.intent_key,
                            message_key=self.message_key,
                            message=self.message
                        )
                        models.MessageDataValue.objects.create(
                            dataset=dataset,
                            data_key=data_key,
                            value_string=value
                        )
                    return self.done_reply(intent_key, message_key, params)

        return self.reply_invalid_option()

    def reply_invalid_option(self):
        """Default reply when the user sends an invalid option.
        """
        # Note: we don't need to set a new context
        return messages.get_body(messages.DO_NOT_UNDERSTAND_OPTION, {})

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

    def save_body_as_string(self, data_key):
        """Save message body in current context with specified data key

        Parameters
        ----------
        data_key
            Data key to store the message body against
        """
        model_utils.save_body_as_string(
            self.message,
            self.intent_key,
            self.message_key,
            data_key
        )