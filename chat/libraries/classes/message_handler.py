import typing
from abc import abstractmethod

from chat import models
from relationships import models as relmods
from common import models as commods

from chat.libraries.constants import datas, messages
from chat.libraries.utility_funcs.get_parameters import get_parameters
from chat.libraries.utility_funcs.get_latest_value import get_latest_value
from chat.libraries.utility_funcs.done_to_context import done_to_context
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.get_product_type import get_product_type
from chat.libraries.utility_funcs.match import match

class MessageHandler():
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
    def __init__(
            self,
            message: models.TwilioInboundMessage,
            intent_key: str,
            message_key: str
        ):
        """Initializes the message handler for an incoming message and the
        context the message is received in.

        The context the message is received in depends (mostly) on the last
        message sent to the user.
        
        E.g., we've sent the menu to the user, and received the user's input to
        the menu - so, the context is menu and the message is the user's
        selection from the menu options.

        Parameters
        ----------
        message
            Twilio inbound message we're handling
        intent_key
            Intent key for the context this message is received in
        message_key
            Message key for the context this message is received in
        """
        self.message = message
        self.intent_key = intent_key
        self.message_key = message_key

        # Options for the message handler to work with - if applicable
        self.options = []
        
        # Values for parameterizer to work with - if applicable
        self.params = {}

        self.dataset, _ = models.MessageDataset.objects.get_or_create(
            intent_key=self.intent_key,
            message_key=self.message_key,
            in_message=self.message,
            user=self.message.from_user
        )

    @abstractmethod
    def run(self) -> str:
        """Message handling code. To be overridden by sub-class. Returns message
        body to reply the user with.
        """
        pass
        
    def add_option(
            self,
            match_strs: typing.List[typing.Tuple[str, int]],
            intent_key: str = None,
            message_key: str = None,
            data_key: str = None,
            data_value: str = None,
            params_func: typing.Callable = None,
            intent_key_func: typing.Callable = None,
            message_key_func: typing.Callable = None,
            chosen_func: typing.Callable = None
        ):
        """Add an option to be matched against the message body. To be used with
        reply_option.

        Options are matched against the body text in the order they are added.
        i.e., the first matching option wins.

        Parameters
        ----------
        match_strs
            List of strings-to-match for this option in the format:
            
            [(string_to_match, edit_distance_tolerance), ...]
            
            A string will be matched against the text body with the
            chat.libraries.utility_funcs.match function.
        intent_key
            Intent key for the context to set if this option is chosen. If
            intent_key_func is specified, intent_key will be ignored.
        message_key
            Message key for the context to set if this option is chosen. If
            message_key_func is specified, message_key will be ignored.
        params_func
            If specified, run this function to compute the parameters for the
            message if this option is chosen.
        data_key
            If specified, store either message body or data_value as data value
            to the data key specified by data_key.
        data_value
            Data key to be stored as user's input if data_key is specified.
            If not specified, the message body will be stored as data value.
            If specified, store this data key as the data value to data_key.
        intent_key_func
            If specified, this function will be ran to compute the intent key
            for the context to set.
        message_key_func
            If specified, this function will be ran to compute the message key
            for the context to set. If message_key_func is specified,
            message_key will be ignored.
        chosen_func
            If specified, this function will run after the user has chosen this
            option. chosen_func gets called with 2 parameters - i.e.,

            chosen_func(msg_handler, data_value)

            msg_handler is the message handler processing the options and
            running the function, and data_value is a reference to the data
            value created to store the data key/value pair.
        """
        self.options.append((match_strs, intent_key, message_key, params_func,
            data_key, data_value, intent_key_func, message_key_func,
            chosen_func))

    def done_reply(
            self,
            intent_key: str,
            message_key: str,
            params_func: typing.Callable=None
        ) -> str:
        """Convenience function to call done_to_context and messages.get_body in
        one call - with support for get_parameters use to get parameters for
        the message body

        Parameters
        ----------
        intent_key
            Intent key for the context to set
        message_key
            Message key for the context to set and message body to return
        params_func
            Optional function to compute parameters for the message body.
            intent_key, message_key and params_func will be passed to
            get_parameters to get parameters for the message body.
        """
        params = get_parameters(self, intent_key, message_key, params_func)
        self.done_to_context(intent_key, message_key)
        return render_message(message_key, params)

    def reply_option(self,
            invalid_option_data_key: str = datas.INVALID_CHOICE,
            invalid_option_intent_key: str = None,
            invalid_option_message_key: str = None,
            invalid_option_params_func: str = None
        ) -> str:
        """Ascertain the option that first matches the message body. Options
        are added with the add_option function, and matched in the order they're
        added.

        Where an invalid option has been input - i.e., the message body does not
        match any option:
            - The message body may be saved as a data value if
                invalid_option_data_key is specified
            - The user's context may be changed if BOTH
                invalid_option_intent_key and invalid_option_message_key are
                specified, thus returning a different message body from the
                default do-not-understand message body. In this case,
                invalid_option_params_func may be specified to set the parameters of
                the user's next context message.

        Parameters
        ----------
        invalid_option_data_key
            If the user has input an invalid option and this parameter is
            specified, save the user's input (i.e., message body) under this
            key in the user's current context.
        invalid_option_intent_key
            Must be specified if invalid_option_message_key is set. This
            parameter is optional and is the intent key of the user's next
            context if the user has input an invalid option.
        invalid_option_message_key
            Must be specified if invalid_option_intent_key is set. This
            parameter is optional and is the message key of the user's next
            context if the user has input an invalid option.
        invalid_option_params_func
            If both invalid_option_intent_key and invalid_option_message_key
            are set, this optional parameter function provides the parameters
            to the user's next context message if no parameterizer is set for
            the invalid_option_intent_key/invalid_option_message_key context.

        Returns
        -------
        Message body to reply the user with
        """
        # Iterate options
        for o in self.options:

            # Unwrap this option
            match_strs, \
            intent_key, \
            message_key, \
            params_func, \
            data_key, \
            data_value, \
            intent_key_func, \
            message_key_func, \
            chosen_func = o

            # Iterate each match string in the option
            for match_str, tolerance in match_strs:
                if match(self.message.body, match_str, tolerance):
                    # Message body matches this option
                    
                    ##### Save value #####

                    # If data key is specified for the option, we store the
                    # user's choice. If data_value is specified, that is,
                    # a custom value to be store is specified - we store this
                    # value under the data key in the current context. If not,
                    # we store the data key itself as value.

                    if data_key is not None:
                        if data_value is not None:
                            value = data_value
                        else:
                            value = data_key
                        dv_ref = self.save_value(data_key, value_string=value)

                    ##### Get keys for the user's next context #####
                    
                    # If intent_key_func is specified, run it to get the intent
                    # key of the next context. If not, use intent_key as the
                    # intent_key of the next function. intent_key_func takes
                    # precedence over intent_key.

                    # If message_key_func is specified, run it to get the
                    # message key of the next context. If not, use message_key
                    # as the intent_key of the next function. message_key_func
                    # takes precedence over message_key.

                    if intent_key_func is not None:
                        to_intent_key = intent_key_func()
                    else:
                        to_intent_key = intent_key
                    
                    if message_key_func is not None:
                        to_message_key = message_key_func()
                    else:
                        to_message_key = message_key

                    ##### Run chosen function if it is specified #####
                    if chosen_func is not None:
                        chosen_func(self, dv_ref)

                    return self.done_reply(
                        to_intent_key, to_message_key, params_func)

        # No matching option found - reply invalid-option
        return self.reply_invalid_option(
            invalid_option_data_key,
            invalid_option_intent_key,
            invalid_option_message_key,
            invalid_option_params_func)

    def reply_bad_input(self,
            data_key: str = None,
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Return message body when the user enters a bad input.

        If params_func is specified, run it to get the parameters for the
        message body. Otherwise, attempt to get the parameterizer for the
        context. If the parameterizer is not specified (i.e., found), set no
        parameters.

        If data_key is specified, save message body under it in the current
        context.

        If intent_key and message_key are both specified, change the user's
        context.

        If only the message_key is specified, do not change the user's context,
        but reply with that message.

        If both intent_key and message_key are not specified, do not change the
        user's context, and reply with the default do-not-understand message.

        If only the intent_key is specified, we treat it as if both it and the
        message_key are not specified.

        Parameters
        ----------
        data_key
            If specified, will save message body in current context
        intent_key
            Intent key of the target context in the event of a bad input. If
            set, will change the current context.
        message_key
            Message key of the target context in the event of a bad input.
        params_func
            Template parameters for the template sent in the event of a bad
            input

        Returns
        -------
        Message body to reply the user with
        """
        # Get parameters for message
        params = get_parameters(self, intent_key, message_key, params_func)

        ##### Save message body (optional) #####

        # If data_key is specified, save message body under it in the current
        # context.

        if data_key is not None:
            self.save_body_as_string(data_key)

        ##### Change context (optional) #####

        # If intent_key and message_key are both specified, change the user's
        # context. Otherwise return default do-not-understand message.

        if intent_key is None and message_key is None:
            # Return default do-not-understand message.
            # Do not change context.
            return render_message(messages.DO_NOT_UNDERSTAND_OPTION, params)
        elif intent_key is None and message_key is not None:
            # Return custom message.
            # Do not change context.
            return render_message(message_key, params)

        # Change context and return new context's message
        return self.done_reply(intent_key, message_key, params)

    def reply_invalid_option(
            self,
            data_key: str = None,
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Call reply_bad_input with a default bad/invalid option message."""
        if message_key is None:
            message_key = messages.DO_NOT_UNDERSTAND_OPTION

        return self.reply_bad_input(
            data_key, intent_key, message_key, params_func)

    def reply_invalid_numeric_value(
            self,
            data_key: str = None,
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Call reply_bad_input with a default bad/invalid option message."""
        if message_key is None:
            message_key = messages.DO_NOT_UNDERSTAND_NUMBER

        return self.reply_bad_input(
            data_key, intent_key, message_key, params_func)

    def done_to_context(
            self,
            intent_key: str,
            message_key: str
        ):
        """Switch user's current context to the specified context

        Parameters
        ----------
        intent_key : string
            Intent key for next context
        message_key : string
            Message key for next context
        """
        done_to_context(self.message.from_user, intent_key, message_key)

    def save_value(
            self,
            data_key: str,
            value_string: str = None,
            value_float: float = None,
            value_boolean: bool = None,
            value_id: int = None
        ):
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
            value_id=value_id)

    def save_body_as_string(
            self,
            data_key: str
        ):
        """Save message body as data value string in current context

        Parameters
        ----------
        data_key : String
            Data key for the data value string
        """
        return self.save_value(data_key, value_string=self.message.body)

    def save_body_as_float(
            self,
            data_key: str
        ):
        """Save message body in current context with specified data key as float

        Parameters
        ----------
        data_key
            Data key to store the message body against

        Returns
        -------
        Float value if successful, None if unable to convert body to float value
        """
        # Validate message body is float
        try:
            value = float(self.message.body.strip())
        except ValueError:
            return None

        return self.save_value(data_key, value_float=value)

    def get_product_type(
            self,
            intent_key: str,
            message_key: str,
            data_key: str
        ) -> typing.Tuple[relmods.ProductType, relmods.UnitOfMeasure]:
        """Get latest value entered by the user with
        intent_key/message_key/data_key, and look up product type with the
        value. If found, return tuple (product_type, uom) - where product_type
        is reference to the product type model, and uomm is reference to its
        unit of measure model.

        Parameters
        ----------
        intent_key
            Intent key for user's latest value for looking up product type
        message_key
            Message key for user's latest value for looking up product type
        data_key
            Data key for user's latest value for looking up product type
        """

        # Get latest user input data value string to match against a product
        # type
        value = self.get_latest_value(intent_key, message_key, data_key)

        if value is None:
            # Value does not exist
            return None

        return get_product_type(value.value_string)

    def get_latest_value(
            self,
            intent_key: str,
            message_key: str,
            data_key: str,
            inbound: bool = True
        ):
        """Convenience method to call get_latest_value with this message's
        sender"""
        return get_latest_value(
            intent_key,
            message_key,
            data_key,
            self.message.from_user,
            inbound=inbound
        )