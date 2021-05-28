from django.test import TestCase

from chat import models, views
from chat.tests import utils
from chat.libraries import context_utils, intents, messages
from relationships import models as relmods

class RegisterTestCase(TestCase):
    user = None
    phone_number = None

    def setUp(self):
        self.phone_number = relmods.PhoneNumber.objects.create(
            country_code='12345',
            national_number='12345678790'
        )

        self.user = relmods.User.objects.create(
            phone_number=self.phone_number
        )

    def tearDown(self):
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

    def test_register(self):
        # User says hi
        msg_1_body = 'Hi'
        msg_1 = utils.create_mock_message(self.user, msg_1_body)

        # Reply
        views.reply(msg_1)

        # Test
        intent_key_1, message_key_1 = context_utils.get_context(self.user)
        self.assertEqual(intent_key_1, intents.REGISTER)
        self.assertEqual(message_key_1, messages.REGISTER__GET_NAME)
        self.assertEqual(self.user.name, None)

        # User gives name
        msg_2_body = 'Kevin'
        msg_2 = utils.create_mock_message(self.user, msg_2_body)

        # Reply
        views.reply(msg_2)

        # Test
        intent_key_1, message_key_1 = context_utils.get_context(self.user)
        self.assertEqual(intent_key_1, intents.MENU)
        self.assertEqual(message_key_1, messages.MENU)
        self.assertEqual(self.user.name, msg_2_body)