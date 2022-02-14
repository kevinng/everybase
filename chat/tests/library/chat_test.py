from django.test import TestCase

from relationships import models as relmods
from common import models as commods
from common.libraries.tear_down import tear_down
from chat import models, views
from chat.utilities.start_context import start_context
from chat.utilities.get_context import get_context
from chat.utilities.get_twilml_body import get_twilml_body
from chat.utilities.render_message import render_message
from chat.tests.library.get_target_message_body import get_target_message_body

class ChatTest(TestCase):
    """Base class for chatbot automated test cases."""
    fixtures = [
        'test/auth__user',
        'test/relationships__email',
        'test/relationships__phone_number_type',
        'test/relationships__phone_number',
        'test/relationships__user',
        'test/common__country'
    ]

    def setUp(
            self,
            intent_key : str = None,
            message_key : str = None,
            registered : bool = True
        ):
        """TestCase setUp method with additonal parameters for overriding.

        Parameters
        ----------
        intent_key
            Intent key of this context.
        message_key
            Message key of this context.
        registered
            If true, user is registered.
        """
        super().setUp()

        self.intent_key = intent_key
        self.message_key = message_key

        # Dictionaries to let us associate dummy inbound/outbound messages
        # with intent/message keys, so only 1 message is associated with each
        # unique key-pair
        self.inbound_messages = {}
        self.outbound_messages = {}

        # Note: we need to reload the country fixtures in the child class if
        # we're overriding the fixtures property.
        self.country = commods.Country.objects.get(pk=511) # Australia

        user_pk = 3 if registered else 6
        self.user = relmods.User.objects.get(pk=user_pk)
        self.user_2 = relmods.User.objects.get(pk=4)

        if intent_key is not None and message_key is not None:
            start_context(self.user, intent_key, message_key)

    def tearDown(self):
        tear_down()

    def assert_context(
            self,
            intent_key : str,
            message_key : str
        ):
        """Assert user's current context.

        intent_key : str
            Intent key to assert.
        message_key : str
            Message key to assert.
        """
        i, m = get_context(self.user)
        self.assertEqual(i, intent_key)
        self.assertEqual(m, message_key)

    def assert_context_body(
            self,
            intent_key : str,
            message_key : str,
            body : str,
            params : dict
        ):
        """
        Convenience function to assert context and message body together.

        Parameters
        ----------
        intent_key
            Intent key for the context to assert.
        message_key
            Message key for the context to assert and message to render.
        body
            Message body to assert.
        params
            Parameters dictionary to merge into message template picked up
            with message_key.
        """
        # print(render_message(message_key, params))
        self.assert_context(intent_key, message_key)
        self.assertEqual(body, render_message(message_key, params))

    def receive_reply_assert(
            self,
            body : str,
            intent_key : str,
            message_key : str,
            target_body_intent_key : str = None,
            target_body_message_key : str = None,
            target_body_params_func : str = None,
            target_body_variation_key : str = None,
            content_type : str = None,
            url : str = None
        ):
        """Receive inbound message body from the simulated user, reply the user,
        assert the user's context and the message replied by the chatbot against
        targets.

        Parameters
        ----------
        body
            Message body received from the simulated user.
        intent_key
            The user's context after the chatbot's reply is asserted against
            this intent. By default, the target message which we're assert the
            chatbot's reply against is determined by this intent key; unless
            target_body_intent_key is specified.
        message_key
            The user's context after the chatbot's reply is asserted against
            this message. By default, the target message which we're assert the
            chatbot's reply against is determined by this message key; unless
            target_body_message_key is specified.
        target_body_intent_key
            If specified, this intent will be used intead of intent_key to
            render the target message.
        target_body_message_key
            If specified, this message will be used instead of message_key
            to render the target message.
        target_body_params_func
            If specified, run this function to compute the message parameters
            for the target message.
        target_body_variation_key
            If specified, use this key to select variation of the target
            message.
        content_type
            If content_type AND url are not None, assert media linked to this
            this message with content_type and url as the media's content-type
            and URL respectively.
        url
            Ditto content_type description.
        """
        message = self.setup_inbound_message(
            self.intent_key,
            self.message_key,
            body
        )

        media = None
        if content_type is not None and url is not None:
            media = models.TwilioInboundMessageMedia.objects.create(
                message=message,
                content_type=content_type,
                url=url
            )

        response = views.reply(
            message, no_external_calls=True, no_task_calls=True)

        response_body = get_twilml_body(response)

        # Get the target message body. Use the default intent/message keys if
        # target_body_intent_key and/or target_body_message_key are not
        # specified.

        # print('RESPONSE BODY')
        # print(response_body)

        if target_body_intent_key is None:
            render_intent_key = intent_key
        else:
            render_intent_key = target_body_intent_key
        
        if target_body_message_key is None:
            render_message_key = message_key
        else:
            render_message_key = target_body_message_key

        target_body = get_target_message_body(
            render_intent_key,
            render_message_key,
            target_body_params_func,
            target_body_variation_key
        )

        # print('TARGET BODY')
        # print(target_body)

        # Assert response body
        self.assertEqual(response_body, target_body)

        # Assert context
        self.assert_context(intent_key, message_key)

        # Assert media if it exists
        if media is not None:
            self.assertEqual(media.content_type, content_type)
            self.assertEqual(media.url, url)

    def setup_inbound_message(
            self,
            intent_key : str,
            message_key : str,
            body : str = None
        ):
        """Setup TwilioInboundMessage for this test.

        Parameters
        ----------
        intent_key
            Intent key of the context.
        message_key
            Message key of the context.
        body
            Body of the message.

        Returns
        -------
        message
            Created TwilioInboundMessage reference.
        """
        message = models.TwilioInboundMessage.objects.create(
            body=body,
            from_user=self.user
        )

        if self.inbound_messages.get(intent_key) is None:
            self.inbound_messages[intent_key] = {}

        self.inbound_messages[intent_key][message_key] = message

        return message

    def setup_outbound_message(
            self,
            intent_key : str,
            message_key : str,
            body : str = None
        ):
        """Setup TwilioOutboundMessage for this test.

        Parameters
        ----------
        intent_key
            Intent key of the context.
        message_key
            Message key of the context.
        body
            Body of the message.

        Returns
        -------
        message
            Created TwilioOutboundMessage reference.
        """
        message = models.TwilioOutboundMessage.objects.create(
            body=body,
            from_user=self.sys_user
        )
        
        if self.outbound_messages.get(intent_key) is None:
            self.outbound_messages[intent_key] = {}
        
        self.outbound_messages[intent_key][message_key] = message

        return message

    def get_or_create_message(
            self,
            intent_key : str,
            message_key : str,
            inbound : bool = True
        ):
        """Returns message previously set up via its context (i.e.,
        intent_key/message_key). Set up a new one if it does not exist.

        Parameters
        ----------
        intent_key
            Intent key for the message's context
        message_key
            Message key for the message's context
        inbound
            True if message is inbound (i.e., from user to us), False if message
            is outbound (i.e., from us to user).
        """

        messages = self.inbound_messages if inbound else self.outbound_messages
        
        if messages.get(intent_key) is None:
            # Intent key found
            messages[intent_key] = {}
        elif messages[intent_key].get(message_key) is not None:
            # Both keys found - return existing message
            return messages[intent_key][message_key]

        # Either key is not found, so message is not found - create new
        messages[intent_key][message_key] = \
            self.setup_inbound_message(intent_key, message_key) if inbound \
                else self.setup_outbound_message(intent_key, message_key)
        
        return messages[intent_key][message_key]