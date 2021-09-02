from django.db.models.fields import DateField
from django.test import TestCase
from chat import models, views

from relationships import models as relmods
from payments import models as paymods
from common import models as commods
from amplitude import models as ampmods

from chat.libraries.test_funcs.get_target_body import get_target_body
from chat.libraries.test_funcs.setup_product_type import setup_product_type
from chat.libraries.utility_funcs.get_latest_value import get_latest_value
from chat.libraries.utility_funcs.get_context import get_context
from chat.libraries.utility_funcs.start_context import start_context
from chat.libraries.utility_funcs.get_twilml_body import get_twilml_body

from chat.libraries.test_funcs.setup_user_phone_number import \
    setup_user_phone_number
from chat.libraries.test_funcs.setup_qna import setup_qna
from chat.libraries.test_funcs.setup_match import setup_match
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOptions

class ChatTest(TestCase):
    """Base class for chat test cases"""

    def setUp(
            self,
            intent_key: str = None,
            message_key: str = None,
            name: str = 'Kevin Ng',
            country_code: str = '12345',
            national_number: str = '1234567890',
            registered: bool = False
        ):
        """TestCase setUp method with additonal parameters for overriding

        Parameters
        ----------
        intent_key : String
            Intent key of this context
        message_key : String
            Message key of this context
        name : String
            Name of the mock user
        country_code : String
            Country code of the mock user's phone number
        national_number : String
            National number of the mock user's phone number
        registered: Bool
            If true, user is registered
        """
        super().setUp()

        self.intent_key = intent_key
        self.message_key = message_key

        # References to aid tear down
        self.users = []
        self.product_types = []
        self.uoms = []
        self.keywords = []

        # Dictionaries to let us associate dummy inbound/outbound messages
        # with intent/message keys, so only 1 message is associated with each
        # unique key-pair
        self.inbound_messages = {}
        self.outbound_messages = {}

        # User
        self.user, self.user_ph = self.setup_user_phone_number(
            name, country_code, national_number, registered)

        # Counter-party, e.g., seller if user is buyer, vice versa
        self.user_2, self.user_2_ph = self.setup_user_phone_number(
            'Test User 2', '23456', '2345678901', registered)

        # System user
        self.sys_user, self.sys_user_ph = self.setup_user_phone_number(
            'Everybase System', '34567', '3456789012', registered)

        self.match = None
        self.payment_hash = None

        if intent_key is not None and message_key is not None:
            start_context(self.user, intent_key, message_key)

    def tearDown(self):
        super().tearDown()

        # Delete all models - order matters

        # Nullify references
        for user in relmods.User.objects.all():
            user.current_qna = None
            user.current_match = None
            user.save()

        models.UserContext.objects.all().delete()
        relmods.QuestionAnswerPair.objects.all().delete()
        paymods.PaymentHash.objects.all().delete()
        relmods.Match.objects.all().delete()

        # Nullify references before deletion
        for demand in relmods.Demand.objects.all():
            demand.next_version = None
            demand.save()
        relmods.Demand.objects.all().delete()
        
        # Nullify references before deletion
        for supply in relmods.Supply.objects.all():
            supply.next_version = None
            supply.save()
        relmods.Supply.objects.all().delete()

        ampmods.Session.objects.all().delete()
        models.MessageDataValue.objects.all().delete()
        models.MessageDataset.objects.all().delete()
        models.TwilioOutboundMessage.objects.all().delete()
        models.TwilioInboundMessage.objects.all().delete()
        relmods.Connection.objects.all().delete()
        relmods.PhoneNumberHash.objects.all().delete()
        relmods.Recommendation.objects.all().delete()
        relmods.Lead.objects.all().delete()
        relmods.User.objects.all().delete()
        relmods.PhoneNumber.objects.all().delete()
        commods.MatchKeyword.objects.all().delete()
        relmods.UnitOfMeasure.objects.all().delete()
        relmods.ProductType.objects.all().delete()

    ##### Assert #####

    def assert_context(
            self,
            intent_key: str,
            message_key: str,
            counter_party: bool = False
        ):
        """Assert user's current context with input context

        intent_key
            Intent key for context to assert against user's context
        message_key
            Message key for context to assert against user's context
        counter_party
            If True, will assert the context of the counter-party instead
        """
        user_to_test = self.user if not counter_party else self.user_2
        user_intent_key, user_message_key = get_context(user_to_test)
        self.assertEqual(user_intent_key, intent_key)
        self.assertEqual(user_message_key, message_key)

    def send_assert(
            self,
            response_body: str,
            intent_key: str,
            message_key: str,
            target_body_intent_key: str = None,
            target_body_message_key: str = None,
            target_body_params_func: str = None,
            target_body_variation_key: str = None,
            counter_party: bool = False
        ):
        """Send message to user, and assert - after-send context and target
        message body.

        Target response text is how the message should look like. We store
        these texts at chat.templates.test.

        If a template has no variations, it is stored in a file with its
        message key and the .txt extension. E.g., MENU.txt.

        If a template has variations, it is stored in a folder with its message
        key, with each variation of the template stored in the folder with
        its variation key and the .txt extension. E.g., YOUR_QUESTION/OTG.txt.
        
        Parameters
        ----------
        response_body
            Response body to assert against the target body
        intent_key
            Intent key for after-reply context. User's context after-reply will
            be asserted against this key. Further, the after-reply message
            target response text will be determined with this key.
        message_key
            Message key for after-reply context. User's context after-reply will
            be asserted against this key. Further, the after-reply message
            target response text will be determined with this key.
        target_body_intent_key
            If specified, this intent key will be used intead of intent_key to
            render the after-reply target response text.
        target_body_message_key
            If specified, this message key will be used instead of message_key
            to render the after-reply target response text.
        target_body_params_func
            If specified, we will run this function to compute the parameters
            for the after-reply target response text.
        target_body_variation_key
            If specified, we will use this key to pick-up specific variation
            of the after-reply target response text.
        counter_party
            If True, will assert the context of the counter-party instead
        """
        # print('RESPONSE BODY')
        # print(response_body)

        target_body = get_target_body(
            intent_key,
            message_key,
            target_body_intent_key,
            target_body_message_key,
            target_body_params_func,
            target_body_variation_key
        )
        # print('TARGET BODY')
        # print(target_body)

        self.assertEqual(response_body, target_body)
        self.assert_context(intent_key, message_key, counter_party)

    def receive_reply_assert(
            self,
            body: str,
            intent_key: str,
            message_key: str,
            target_body_intent_key: str = None,
            target_body_message_key: str = None,
            target_body_params_func: str = None,
            target_body_variation_key: str = None
        ):
        """Receive inbound message, reply, assert - after-reply context and
        target message text.

        Parameters
        ----------
        body
            Message body of message we receive from user
        intent_key
            Intent key for after-reply context. User's context after-reply will
            be asserted against this key. Further, the after-reply message
            target response text will be determined with this key.
        message_key
            Message key for after-reply context. User's context after-reply will
            be asserted against this key. Further, the after-reply message
            target response text will be determined with this key.
        target_body_intent_key
            If specified, this intent key will be used intead of intent_key to
            render the after-reply target response text.
        target_body_message_key
            If specified, this message key will be used instead of message_key
            to render the after-reply target response text.
        target_body_params_func
            If specified, we will run this function to compute the parameters
            for the after-reply target response text.
        target_body_variation_key
            If specified, we will use this key to pick-up specific variation
            of the after-reply target response text.
        """
        response = self.receive_reply(body)
        response_body = get_twilml_body(response)

        self.send_assert(
            response_body,
            intent_key,
            message_key,
            target_body_intent_key,
            target_body_message_key,
            target_body_params_func,
            target_body_variation_key
        )

    def assert_latest_value(
            self,
            intent_key: str,
            message_key: str,
            data_key: str,
            value_string: str = None,
            value_float: float = None,
            value_boolean=None,
            value_id=None
        ):
        """Assert latest data value for intent_key+message_key+data_key -
        against input value_string/value_float/value_boolean/value_id.

        One of either value_string/value_float/value_boolean/value_id must be
        specified, and they are evaluated in that order. The first match will
        return. E.g., if value_float and value_boolean are both specified,
        only value_float will be matched and returned.

        Parameters
        ----------
        intent_key
            Intent key for data value's context
        message_key
            Message key for data value's context
        data_key
            Data key for data value
        value_string
            String value to assert against data value's string value
        value_float
            Float value to assert against data value's float value
        value_boolean
            Boolean value to assert against data value's boolean value
        """
        data_value = get_latest_value(
            intent_key,
            message_key,
            data_key,
            self.user
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
        elif value_id is not None:
            self.assertEqual(data_value.value_id, value_id)
            return

        self.fail('Exactly 1 value must be provided')

    def assert_value(
            self,
            data_key: str,
            value_string: str = None,
            value_float: float = None,
            value_boolean: bool = None,
            value_id: int = None
        ):
        """Convenience method to call assert_latest_value in this context
        against the value at the specified data_key.

        Parameters
        ----------
        data_key
            Data key for the value
        value_string
            String value to assert against data value's string value
        value_float
            Float value to assert against data value's float value
        value_boolean
            Boolean value to assert against data value's boolean value
        value_id
            Int ID value to assert against data value's ID value
        """
        self.assert_latest_value(
            self.intent_key,
            self.message_key,
            data_key,
            value_string=value_string,
            value_float=value_float,
            value_boolean=value_boolean,
            value_id=value_id
        )

    def setup_user_phone_number(
            self,
            name: str = 'Kevin Ng',
            country_code: str = '12345',
            national_number: str = '1234567890',
            registered: bool = True
        ):
        """Create user and phone number

        Parameters
        ----------
        name
            User's name
        country_code
            Country code of the user's phone number
        national_number
            National number of the user's phone number
        registered
            True if user is registered
        """
        user, phone_number = setup_user_phone_number(
            name, country_code, national_number, registered)
        
        # Add reference to aid tear down
        self.users.append(user)

        return (user, phone_number)

    def setup_inbound_message(self, intent_key, message_key, body=None):
        message = models.TwilioInboundMessage.objects.create(
            body=body,
            from_user=self.user
        )

        if self.inbound_messages.get(intent_key) is None:
            self.inbound_messages[intent_key] = {}

        self.inbound_messages[intent_key][message_key] = message

        return message

    def setup_outbound_message(self, intent_key, message_key, body=None):
        message = models.TwilioOutboundMessage.objects.create(
            body=body,
            from_user=self.sys_user
        )
        
        if self.outbound_messages.get(intent_key) is None:
            self.outbound_messages[intent_key] = {}
        
        self.outbound_messages[intent_key][message_key] = message

        return message
        
    def setup_data_value(
            self,
            intent_key,
            message_key,
            data_key,
            value_string=None,
            value_float=None,
            value_boolean=None,
            value_id=None,
            inbound: bool = True
        ):
        """Set up mock data value string in context for a message

        Parameters
        ----------
        intent_key : String
            Intent key for data value's context
        message_key : String
            Message key for data value's context
        data_key : String
            Data key for data value
        value_string : String
            Data value string
        value_float : Float
            Data value float
        value_boolean : Boolean
            Data value boolean
        value_id : Integer
            Data value integer
        inbound : Boolean
            If true, set value for a mock inbound message. If false, set value
            for a mock outbound message
        """
        # Get or create dataset
        message = self.get_create_message(intent_key, message_key, inbound)
        if inbound:
            dataset, _ = models.MessageDataset.objects.get_or_create(
                intent_key=intent_key,
                message_key=message_key,
                in_message=message,
                user=self.user
            )
        else:
            dataset, _ = models.MessageDataset.objects.get_or_create(
                intent_key=intent_key,
                message_key=message_key,
                out_message=message,
                user=self.sys_user
            )

        return models.MessageDataValue.objects.create(
            dataset=dataset,
            data_key=data_key,
            value_string=value_string,
            value_float=value_float,
            value_boolean=value_boolean,
            value_id=value_id
        )

    def setup_product_type(
            self,
            name: str = None,
            uom_name: str = None,
            uom_plural_name: str = None,
            uom_description: str = None,
            keyword: str = None
        ):
        """Set up product type, unit of measure and matching keyword

        Returns
        -------
        (product_type, unit_of_measure, keyword)
            product_type
                Product type model reference set up
            unit_of_measure
                Unit of measure model reference set up
            keyword
                Match keyword model reference set up
        """
        if name is None:
            name = 'Product %d' % len(self.product_types)
        
        if uom_name is None:
            uom_name = 'Product %d UOM' % len(self.product_types)
        
        if uom_plural_name is None:
            uom_plural_name = 'Product %d UOMs' % len(self.product_types)
        
        if uom_description is None:
            uom_description = 'Product %d UOM description' % \
                len(self.product_types)

        if keyword is None:
            keyword = 'product %d' % len(self.product_types)

        product_type, uom, keyword = setup_product_type(
            name, uom_name, uom_plural_name, uom_description, keyword)
        
        self.product_types.append(product_type)
        self.uoms.append(uom)
        self.keywords.append(keyword)

        return (product_type, uom, keyword)

    def setup_match(
        self,
        buying: bool,
        supply_type: SupplyAvailabilityOptions,
        closed: bool = False
    ) -> relmods.Match:
        """Set up a user as either a buyer or a seller, and user_2 as the
        counter-party (i.e., seller if user is buyer, vice versa).

        Parameters
        ----------
        buying
            If true, set up user as the buyer, otherwise - set him up as the
            seller.
        supply_type
            The type of supply either the user/user_2 is selling - depending
            on who's the buyer.
        closed
            Close the match immediately.
        """

        self.match = setup_match(
            buying, supply_type, self.user, self.user_2, closed)

        self.user.current_match = self.match
        self.user.save()

        self.user_2.current_match = self.match
        self.user_2.save()

        return self.match

    def setup_payment_hash(self) -> paymods.PaymentHash:
        """Set up payment hash for this user and match"""
        price = paymods.Price.objects.create(display_name='USD 5.67')
        self.payment_hash = paymods.PaymentHash.objects.create(
            user=self.user,
            match=self.match,
            price=price
        )

        return self.payment_hash

    def setup_qna(
            self,
            answering: bool = True,
            answered: bool = False,
            question_captured: str = 'Can you do OEM?',
            answer_captured: str = 'Yes, we can.',
            manual_cleaned_question: str = 'Can you do OEM? (Manual-Cleaned)',
            manual_cleaned_answer: str = 'Yes, we can. (Manual-Cleaned)',
            auto_cleaned_question: str = 'Can you do OEM? (Auto-Cleaned)',
            auto_cleaned_answer: str = 'Yes, we can. (Auto-Cleaned)',
            answer_readied: bool = None,
            question_readied: bool = None
        ) -> relmods.QuestionAnswerPair:
        """Set up QNA model and associated data key/value for this user, user_2
        and match.

        Returns
        -------
        Q&A model reference set up
        """

        qna = setup_qna(
            self.user,
            self.user_2,
            self.match,
            answering,
            answered, 
            question_captured,
            answer_captured,
            manual_cleaned_question,
            manual_cleaned_answer,
            auto_cleaned_question,
            auto_cleaned_answer,
            answer_readied,
            question_readied
        )

        # Set up user's current_qna
        self.user.current_qna = qna
        self.user.save()

        return qna

    def get_create_message(
            self,
            intent_key: str,
            message_key: str,
            inbound: bool = True
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

    def receive_reply(
            self,
            body: str
        ):
        """Receive inbound message in this context and reply with message body
        
        body
            Message body
        """
        message = self.setup_inbound_message(
            self.intent_key,
            self.message_key,
            body
        )
        return views.reply(message, no_external_calls=True, no_task_calls=True)