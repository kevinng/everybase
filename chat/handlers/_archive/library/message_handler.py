import typing
from abc import abstractmethod

from django.http.request import HttpRequest
from common.utilities.get_ip_address import get_ip_address

from amplitude.tasks.send_event import send_event
from amplitude.utilities import get_user_properties

from chat import models
from chat.constants import messages
from chat.utilities.get_parameters import get_parameters
from chat.utilities.done_to_context import done_to_context
from chat.utilities.render_message import render_message
from chat.utilities.match import match

class MessageHandler():
    """A message handler lets us handle an incoming message by overriding the
    run function.
    """
    def __init__(
            self,
            message : models.TwilioInboundMessage,
            intent_key : str,
            message_key : str,
            no_external_calls : bool = False,
            no_task_calls : bool = False,
            request : HttpRequest = None
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
            Twilio inbound message we're handling.
        intent_key
            Intent key for the context this message is received in.
        message_key
            Message key for the context this message is received in.
        no_external_calls
            If True, will not make external calls. Set to True in tests.
        no_task_calls
            If True, will not make background task calls. Set to True in tests.
        request
            HttpRequest object that initiated this message handler.
        """
        self.message = message
        self.intent_key = intent_key
        self.message_key = message_key
        self.no_external_calls = no_external_calls
        self.no_task_calls = no_task_calls
        self.request = request

        # Options for the message handler to work with - if applicable.
        self.options = []
        
        # Values for parameterizer to work with - if applicable.
        self.params = {}

    @abstractmethod
    def run(self) -> str:
        """Message handling code. To be overridden by the sub-class.

        Returns
        -------
        body
            Message body to reply the user with.
        """
        pass
        
    def add_option(
            self,
            match_strs : typing.List[typing.Tuple[str, int]],
            intent_key : str = None,
            message_key : str = None,
            params_func : typing.Callable = None,
            intent_key_func : typing.Callable = None,
            message_key_func : typing.Callable = None,
            chosen_func : typing.Callable = None,
            event_key : str = None,
            event_properties: dict = None,
            user_properties: dict = None
        ):
        """We may expect the user to reply with one of an option presented in
        the previous message. In this case, the user's input should be limited
        to a set of options, and anything else should be responded as a
        standard do-not-understand message.

        This function adds an option that the user can reply with to this
        message handler.

        The reply_option can be called to return the message body to respond to
        the user with.
        
        Options are matched against the body text in the order they are added.
        i.e., the first matching option wins.

        Parameters
        ----------
        match_strs
            List of strings-to-match for this option in the format:
            
            [(string_to_match, edit_distance_tolerance), ...]
            
            A string will be matched against the text body with the
            chat.utilities.match function. string_to_match and
            edit_distance_tolerance provides the string-to-match and
            edit-distance-tolerance input to the match function respectively.
        intent_key
            Intent key for the context to set if this option is chosen. If
            intent_key_func is specified, it will be used to compute the intent
            key for the context to set, and intent_key will be ignored.
        message_key
            Message key for the context to set if this option is chosen. If
            message_key_func is specified, it will be used to compute the intent
            key for the context to set, and message_key will be ignored.
        params_func
            If specified, this function will be run to compute the parameters to
            merge with the reply message template for chosen option.
        intent_key_func
            If specified, this function will be ran to compute the intent key
            for the context to set.
        message_key_func
            If specified, this function will be ran to compute the message key
            for the context to set. If message_key_func is specified,
            message_key will be ignored.
        chosen_func
            If specified, this function will run after the user has chosen this
            option. chosen_func has 1 parameter:

            chosen_func(msg_handler)

            msg_handler is the message handler processing the options (i.e.,
            self).
        event_key
            If specified, will make Amplitude event call with this event key
            when this option is chosen, together with the event_properties and
            user_properties parameter inputs if they are specified as well.
        event_properties
            If event_key is specified, use this dictionary as the event
            properties for the Amplitude event call if this option is chosen.
        user_properties
            If event_key is specified, use this dictionary as the user
            properties for the Amplitude event call if this option is chosen.
        """
        self.options.append((match_strs, intent_key, message_key, params_func,
            intent_key_func, message_key_func, chosen_func, event_key,
            event_properties, user_properties))

    def reply_option(
            self,
            invalid_option_intent_key : str = None,
            invalid_option_message_key : str = None,
            invalid_option_params_func : str = None
        ) -> str:
        """Ascertain the option that first matches the message body. Options
        are added with the add_option function, and matched in the order they're
        added.

        Where an invalid option has been input (i.e., the message body does not
        match any option), return the default do-not-understand message body
        and do NOT change the user's context - unless BOTH
        invalid_option_intent_key and invalid_option_message_key are specified,
        in which case the user's context will be switched to them, and they
        will be used to render the reply message.

        Parameters
        ----------
        invalid_option_intent_key
            Optional. Must be specified if invalid_option_message_key is set.
        invalid_option_message_key
            Optional. Must be specified if invalid_option_intent_key is set.
        invalid_option_params_func
            Optional. If both invalid_option_intent_key and
            invalid_option_message_key are set, this optional parameter function
            will be run to compute the parameters to merge into the reply
            message template.

        Returns
        -------
        Message body to reply the user with.
        """
        # Iterate options
        for o in self.options:

            # Unwrap this option
            match_strs,\
            intent_key,\
            message_key,\
            params_func,\
            intent_key_func,\
            message_key_func,\
            chosen_func,\
            event_key,\
            event_properties,\
            user_properties = o

            # Iterate each match string in the option
            for match_str, tolerance in match_strs:
                if match(self.message.body, match_str, tolerance):
                    # Message body matches this option.
                    
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

                    # If event_key is specified - send Amplitude event.
                    # if event_key is not None:
                    #     self.send_amplitude_event(
                    #         event_key,
                    #         event_properties,
                    #         user_properties
                    #     )

                    # If chosen_func is specified - run it.
                    if chosen_func is not None:
                        chosen_func(self)

                    return self.done_reply(
                        to_intent_key, to_message_key, params_func)

        # No matching option found - reply invalid-option.
        return self.reply_invalid_option(
            invalid_option_intent_key,
            invalid_option_message_key,
            invalid_option_params_func
        )

    def done_reply(
            self,
            intent_key: str,
            message_key: str,
            params_func: typing.Callable=None,
            done_func: typing.Callable=None
        ) -> str:
        """Set the user's current context as done, switch the user to the next
        context, then render and return the reply message.

        Parameters
        ----------
        intent_key
            Intent key for the context to set
        message_key
            Message key for the context to set and message body to return
        params_func
            If specified, this function will be run to compute the parameters to
            merge with the reply message template.
        done_func
            If specified, this function will be called after the user's new
            context is set.
        """
        # Get parameters for the reply message.
        params = get_parameters(self, intent_key, message_key, params_func)

        # Set current context as done, and switch the user to the next context.
        done_to_context(self.message.from_user, intent_key, message_key)

        # Call done_func if it is set.
        if done_func is not None:
            done_func()
        
        # Render and return reply message body.
        return render_message(message_key, params)

    def send_amplitude_event(
            self,
            event_key : str,
            event_properties : dict = None,
            user_properties : dict = None
        ):
        """Send amplitude event.
        
        event_key
            Amplitude event key.
        event_properties
            Amplitude event properties.
        user_properties
            Amplitude user properties.
        """
        if self.no_external_calls:
            return None

        # Assign this message's context to the event properties.
        event_properties[keys.INTENT] = self.intent_key
        event_properties[keys.MESSAGE] = self.message_key

        # Assign values to user properties.
        user_properties = get_user_properties(self.message.from_user)

        # Set user agent data to event properties if self.request is not None.
        if self.request is not None:
            ua = self.request.user_agent
            event_properties = {
                'ip_address': get_ip_address(self.request),
                'is_mobile': ua.is_mobile,
                'is_tablet': ua.is_tablet,
                'is_touch_capable': ua.is_touch_capable,
                'is_pc': ua.is_pc,
                'is_bot': ua.is_bot,
                'browser': ua.browser,
                'browser_family': ua.browser.family,
                'browser_version': ua.browser.version,
                'browser_version_string': ua.browser.version_string,
                'os': ua.os,
                'os_family': ua.os.family,
                'os_version': ua.os.version,
                'os_version_string': ua.os.version_string,
                'device': ua.device,
                'device_family': ua.device.family
            }
        else:
            event_properties = {}

        # Send Amplitude event.
        send_event.delay(
            user_id=self.message.from_user.id,
            event_type=event_key,
            event_properties=event_properties,
            user_properties=user_properties,
            os_name=ua.os,
            os_version=ua.os.version_string,
            device_brand=ua.device.family,
            device_manufacturer=ua.device.family,
            device_model=ua.device,
            ip=get_ip_address(self.request)
        )

    def reply_bad_input(
            self,
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Return message body when the user enters a bad input.

        If params_func is specified, run it to get the parameters for the
        message body. Otherwise, attempt to get the parameterizer for the
        context. If the parameterizer is not specified (i.e., found), set no
        parameters.

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
        body
            Message body to reply the user with.
        """
        # Get parameters for message
        params = get_parameters(self, intent_key, message_key, params_func)

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
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Call reply_bad_input with a default bad/invalid option message."""
        if message_key is None:
            message_key = messages.DO_NOT_UNDERSTAND_OPTION

        # TODO
        # self.send_amplitude_event(events.DO_NOT_UNDERSTAND_OPTION)

        return self.reply_bad_input(intent_key, message_key, params_func)

    def reply_invalid_numeric_value(
            self,
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Call reply_bad_input with a default bad/invalid option message."""
        if message_key is None:
            message_key = messages.DO_NOT_UNDERSTAND_NUMBER

        # TODO
        # self.send_amplitude_event(events.INVALID_NUMERIC_VALUE)

        return self.reply_bad_input(intent_key, message_key, params_func)

    def reply_invalid_email(
            self,
            intent_key: str = None,
            message_key: str = None,
            params_func: typing.Callable = None
        ) -> str:
        """Call reply_bad_input with a default bad/invalid option message."""
        if message_key is None:
            message_key = messages.DO_NOT_UNDERSTAND_EMAIL

        # TODO
        # self.send_amplitude_event(events.INVALID_EMAIL)

        return self.reply_bad_input(intent_key, message_key, params_func)
