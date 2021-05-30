from django.test import TestCase

from chat import models, views
from chat.libraries import context_utils, model_utils
from relationships import models as relmods

def create_mock_message(user, body):
    """Create mock TwilioInboundMessage for the purposes of testing.

    Parameters
    ----------
    user : relationships.User
        User sending this message
    body : string
        Message body
    """
    return models.TwilioInboundMessage.objects.create(
        from_user=user,
        body=body
    )

class ChatFlowTest(TestCase):
    """Base class with helper functions for chat-flow tests.
    """
    user = None
    phone_number = None

    def setUp(self):
        self.setup_user(None)

    def tearDown(self):
        self.tear_down_user()

    def setup_user(self, name='Test User'):
        """Set up user and its relevant models
        """

        self.phone_number = relmods.PhoneNumber.objects.create(
            country_code='12345',
            national_number='12345678790'
        )

        self.user = relmods.User.objects.create(
            phone_number=self.phone_number,
            name=name
        )

    def tear_down_user(self):
        """Tear down user and its relevant models
        """

        # Get all messages from this user
        messages = models.TwilioInboundMessage.objects.filter(
            from_user=self.user
        )

        # Delete dataset and values
        for m in messages:
            datasets = models.MessageDataset.objects.filter(message=m)
            for d in datasets:
                models.MessageDataValue.objects.filter(dataset=d).delete()
                d.delete()

        # Delete messages
        messages.delete()

        # Delete user contexts
        models.UserContext.objects.filter(
            user=self.user
        ).delete()

        # Delete user and phone numbers
        self.user.delete()
        self.phone_number.delete()

    def assert_context(self, intent_key, message_key):
        """Assert users context with input context

        intent_key : String
            Intent key for context to assert against user's context
        message_key : String
            Message key for context to assert against user's context
        """
        user_intent_key, user_message_key = context_utils.get_context(self.user)
        self.assertEqual(user_intent_key, intent_key)
        self.assertEqual(user_message_key, message_key)

    def receive(self, body):
        """Receive mock message

        body : String
            Message body
        """
        return create_mock_message(self.user, body)

    def reply(self, message):
        """Reply message

        Parameters
        ----------
        message : TwilioInboundMessage
            Message to reply
        """
        return views.reply(message)

    def receive_reply(self, body):
        """Receive mock message and reply
        
        body : String
            Message body
        """
        return self.reply(self.receive(body))

    def receive_reply_assert(self, body, intent_key, message_key):
        """Receive mock message, reply and assert context

        Parameters
        ----------
        body : String
            Message body
        intent_key : String
            Intent key for context to assert against user's context
        message_key : String
            Message key for context to assert against user's context
        """
        self.receive_reply(body)
        self.assert_context(intent_key, message_key)

    def assert_latest_value(self, intent_key, message_key, data_key,
        value_string=None, value_float=None, value_boolean=None):
        """Assert latest data value for - intent_key, message_key, data_key -
        against input

        Parameters
        ----------
        intent_key : String
            Intent key for data value's context
        message_key : String
            Message key for data value's context
        data_key : String
            Data key for data value
        value_string : String
            String value to assert against data value's string value
        value_float : Float
            Float value to assert against data value's float value
        value_boolean : Boolean
            Boolean value to assert against data value's boolean value
        """
        data_value = model_utils.get_latest_value(
            intent_key,
            message_key,
            data_key
        )

        if data_value is None:
            self.fail('Value does not exist')

        if value_string is not None:
            self.assertEqual(data_value.value_string, value_string)
            return
        elif value_float is not None:
            self.assertEqual(data_value.value_float, value_float)
            return
        elif value_boolean is not None:
            self.assertEqual(data_value.value_boolean, value_boolean)
            return

        self.fail('Exactly 1 value must be provided')