from chat import models

from chat.libraries import messages, nlp
from chat.libraries.utilities.get_latest_value import get_latest_value
from chat.libraries.utilities.get_context import get_context
from chat.libraries.utilities.start_context import start_context
from chat.libraries.utilities.done_context import done_context

from relationships import models as relmods
from common import models as commods

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
        self.env_vars = {}
        self.env_var_funcs = {}

        self.dataset = self.get_or_create_dataset()

    def run(self):
        """Message handling logic - to be overridden
        """
        return None

    def set_env_var(self, key, value=None, value_func=None):
        """Set environment variable. If value is lazy-loaded, set value to None
        and set a value_func and it will be used to lazy-load the value.
        
        An exception will be raised if both value and value_func are None.

        Parameters
        ----------
        key : String, optional
            Key
        value : String, optional
            Value
        value_func : Function, optional
            Value function which will be used to set value lazy-loaded. Value
                must not be set if it is to be lazy-loaded.
        """
        if value is None and value_func is None:
            raise Exception('value_func must be set if value is not set')
        
        self.env_vars[key] = value
        self.env_var_funcs[key] = value_func

    def get_env_var(self, key):
        """Get environment variable. If it does not exist, will set with with
        pre-defined environment variable function.

        Parameters
        ----------
        key
            Key for value/value-function
        """
        value = self.env_vars.get(key)
        if value is None:
            # Value does not exist for key, set it with the value function
            # Note: if value is not set, value function MUST be set, or an error
            #   will be raised
            self.env_vars[key] = self.env_var_funcs[key]()
            return self.env_vars[key]

        return value
        
    def add_option(self, match_strs, intent_key, message_key, params,
        data_key=None, data_value=None, intent_key_func=None,
        message_key_func=None):
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
        intent_key_func : function, optional
            If present, will be used to ascertain the intent key - ignoring
            intent_key
        message_key_func : function, optional
            If present, will be used to ascertain the message key - ignoring
            message_key
        """
        self.options.append(
            (match_strs, intent_key, message_key, params, data_key, data_value,
                intent_key_func, message_key_func))

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

    def reply_option(self, invalid_option_intent_key=None,
        invalid_option_message_key=None, invalid_option_params=None):
        """Run nlp.match_each_token against each option in against message body.

        Set context and return message body of the FIRST matching option.

        If data key/value is/are provided for an option, store user's choice.

        If no matching option is found - return reply_invalid_option value,
        passing in invalid_option_intent_key and invalid_option_message_key to set
        the reply message if necessary.

        Parameters
        ----------
        invalid_option_intent_key : String, optional
            Intent key of the target context in the event of a invalid option. 
            If set, will change the current context.
        invalid_option_message_key : String, optional
            Message key of the target context in the event of a invalid option.
        invalid_option_params : String, optional
            Template parameters for the template sent in the event of a
            invalid option
        """
        for o in self.options:
            match_strs, intent_key, message_key, params_func, data_key, \
                data_value, intent_key_func, message_key_func = o
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

                    # Get parameters for template
                    if params_func is not None:
                        params = params_func()
                    else:
                        params = {}

                    # Get context keys
                    if intent_key_func is not None:
                        to_intent_key = intent_key_func()
                    else:
                        to_intent_key = intent_key
                    
                    if message_key_func is not None:
                        to_message_key = message_key_func()
                    else:
                        to_message_key = message_key

                    return self.done_reply(
                        to_intent_key, to_message_key, params)

        return self.reply_invalid_option(invalid_option_intent_key,
            invalid_option_message_key, invalid_option_params)

    def reply_invalid_option(self, invalid_option_intent_key=None,
        invalid_option_message_key=None, invalid_option_params=None):
        """Default reply when the user sends an invalid option.

        Parameters
        ----------
        invalid_option_intent_key : String, optional
            Intent key of the target context in the event of a invalid option.
            If set, will change the current context.
        invalid_option_message_key : String, optional
            Message key of the target context in the event of a invalid option.
        invalid_option_params : String, optional
            Template parameters for the template sent in the event of a
            invalid option
        """
        if invalid_option_params is None:
            invalid_option_params = {}

        # If invalid_option_intent_key is set, change the current context. If not,
        # the user stays in the current context.
        if invalid_option_intent_key is None and \
            invalid_option_message_key is None:
            return messages.get_body(messages.DO_NOT_UNDERSTAND_OPTION, {})
        elif invalid_option_intent_key is None and \
            invalid_option_message_key is not None:
            return messages.get_body(
                invalid_option_message_key, invalid_option_params)

        return self.done_reply(invalid_option_intent_key,
            invalid_option_message_key, invalid_option_params)

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
        now_intent_key, now_message_key = get_context(self.message.from_user)

        # Done current context
        done_context(self.message.from_user, now_intent_key, now_message_key)

        # Start next context
        start_context(self.message.from_user, intent_key, message_key)

    def get_or_create_dataset(self):
        """Get/create dataset for this message
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
        # Validate message body is float
        try:
            value = float(self.message.body.strip())
        except ValueError:
            return None

        return self.save_value(data_key, value_float=value)

    def get_product_type(self, intent_key, message_key, data_key):
        # Get latest user input data value string to match against a product
        # type
        value = self.get_latest_value(intent_key, message_key, data_key)

        if value is None:
            # Value does not exist
            return None

        value_string = value.value_string

        # Get all match keywords for product types
        match_keywords = commods.MatchKeyword.objects.filter(
            product_type__isnull=False
        )

        # Match each keyword against user input
        product_type = None
        for k in match_keywords:
            if nlp.match(value_string, k.keyword, k.tolerance):
                # User input match a product type
                product_type = k.product_type

        uom = None
        if product_type is not None:
            # Matching product type found - get its top UOM
            try:
                uom = relmods.UnitOfMeasure.objects.filter(
                    product_type=product_type
                ).order_by('-priority').first()
            except relmods.UnitOfMeasure.DoesNotExist:
                pass
        
        return (product_type, uom)

    def get_latest_value(self, intent_key, message_key, data_key, inbound=True):
        """Convenience method to call get_latest_value with this message's
        sender.
        """
        return get_latest_value(
            intent_key,
            message_key,
            data_key,
            self.message.from_user,
            inbound
        )