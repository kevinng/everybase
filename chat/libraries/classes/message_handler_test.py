import typing
from enum import Enum

import pytz, datetime
from everybase.settings import TIME_ZONE
from django.test import TestCase
from django.template.loader import render_to_string

from chat import models, views
from chat.libraries.constants import intents, messages
from chat.libraries.utilities.get_latest_value import get_latest_value
from chat.libraries.utilities.get_context import get_context
from chat.libraries.utilities.start_context import start_context

from relationships import models as relmods
from payments import models as paymods
from common import models as commods

class SupplyAvailabilityOption(Enum):
    OTG = 1
    PRE_ORDER_DEADLINE = 2
    PRE_ORDER_DURATION = 3

SupplyAvailabilityOptions = typing.NewType(
    'SupplyAvailabilityOptions', SupplyAvailabilityOption)

class MessageHandlerTest(TestCase):
    """Base class for message handler test cases"""

    def setUp(
            self,
            intent_key: str = None,
            message_key: str = None,
            name: str = 'Kevin Ng',
            country_code: str = '12345',
            national_number: str = '1234567890'
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
            name, country_code, national_number)

        # Counter-party, e.g., seller if user is buyer, vice versa
        self.user_2, self.user_2_ph = self.setup_user_phone_number(
            'Test User 2', '23456', '2345678901')

        # System user
        self.sys_user, self.sys_user_ph = self.setup_user_phone_number(
            'Everybase System', '65', '88933466')

        self.match = None
        self.payment_hash = None

        if intent_key is not None and message_key is not None:
            start_context(self.user, intent_key, message_key)

    def tearDown(self):
        super().tearDown()

        # Clear database

        # Nullify references
        for user in relmods.User.objects.all():
            user.current_qna = None
            user.current_match = None
            user.save()

        # Delete all - order matters
        models.UserContext.objects.all().delete()
        relmods.QuestionAnswerPair.objects.all().delete()
        paymods.PaymentHash.objects.all().delete()
        relmods.Match.objects.all().delete()
        relmods.Demand.objects.all().delete()        
        relmods.Supply.objects.all().delete()
        models.MessageDataValue.objects.all().delete()
        models.MessageDataset.objects.all().delete()
        models.TwilioOutboundMessage.objects.all().delete()
        models.TwilioInboundMessage.objects.all().delete()
        relmods.Connection.objects.all().delete()
        relmods.PhoneNumberHash.objects.all().delete()
        relmods.User.objects.all().delete()
        relmods.PhoneNumber.objects.all().delete()
        commods.MatchKeyword.objects.all().delete()
        relmods.UnitOfMeasure.objects.all().delete()
        relmods.ProductType.objects.all().delete()

    ##### Assert #####

    def assert_context(
            self,
            intent_key: str,
            message_key: str
        ):
        """Assert user's current context with input context

        intent_key
            Intent key for context to assert against user's context
        message_key
            Message key for context to assert against user's context
        """
        user_intent_key, user_message_key = get_context(self.user)
        self.assertEqual(user_intent_key, intent_key)
        self.assertEqual(user_message_key, message_key)

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
        target response text.

        Target response text is how the message should look like. We store
        these texts at chat.templates.test.

        If a template has no variations, it is stored in a file with its
        message key and the .txt extension. E.g., MENU.txt.

        If a template has variations, it is stored in a folder with its message
        key, with each variation of the template stored in the folder with
        its variation key and the .txt extension. E.g., YOUR_QUESTION/OTG.txt.

        Parameters
        ----------
        body
            Message body
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
        # print('FULL RESPONSE')
        # print(response)

        if target_body_intent_key is None:
            render_intent_key = intent_key
        else:
            render_intent_key = target_body_intent_key
        
        if target_body_message_key is None:
            render_message_key = message_key
        else:
            render_message_key = target_body_message_key

        # Render body from target path
        target_path = 'chat/messages/test/%s/%s' % \
            (render_intent_key, render_message_key)
        if target_body_variation_key is None:
            target_path += '.txt'
        else:
            target_path += '/%s.txt' % target_body_variation_key

        if target_body_params_func is None:
            target_params = {}
        else:
            target_params = target_body_params_func()
        target_body = render_to_string(target_path, target_params)

        # print('TARGET BODY')
        # print(target_body)

        # Get body from response TwilML
        start_pos = response.index('<Message>') + len('<Message>')
        end_pos = response.index('</Message>')
        response_body = response[start_pos:end_pos]

        # print('RESPONSE BODY')
        # print(response_body)

        self.assertEqual(response_body, target_body)
        self.assert_context(intent_key, message_key)

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
        against the valeu at the specified data_key.

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

    ##### Set up #####

    def setup_user_phone_number(
            self,
            name: str = 'Kevin Ng',
            country_code: str = '12345',
            national_number: str = '1234567890'
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
        """
        phone_number = relmods.PhoneNumber.objects.create(
            country_code=country_code,
            national_number=national_number)

        user = relmods.User.objects.create(
            phone_number=phone_number,
            name=name)
        
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
        message = self.get_message(intent_key, message_key, inbound)
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
        
        product_type = relmods.ProductType.objects.create(name=name)
        self.product_types.append(product_type)

        uom = relmods.UnitOfMeasure.objects.create(
            name=uom_name,
            plural_name=uom_plural_name,
            description=uom_description,
            product_type=product_type)
        
        self.uoms.append(uom)

        # Create match keyword for test product type
        keyword = commods.MatchKeyword.objects.create(
            keyword=keyword,
            tolerance=0,
            product_type=product_type)
        self.keywords.append(keyword)

        return (product_type, uom, keyword)

    def setup_user_lead(
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

        # Product type and packing for both supply and demand
        product_type, packing, _ = self.setup_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )

        # Supply availability
        if supply_type == SupplyAvailabilityOption.OTG:
            availability = relmods.Availability.objects.get(pk=1)
        elif supply_type == SupplyAvailabilityOption.PRE_ORDER_DEADLINE or \
            supply_type == SupplyAvailabilityOption.PRE_ORDER_DURATION:
            availability = relmods.Availability.objects.get(pk=2)

        # Supply timeframe
        pre_order_timeframe = None
        sgtz = pytz.timezone(TIME_ZONE)
        if supply_type == SupplyAvailabilityOption.PRE_ORDER_DEADLINE:
            pre_order_timeframe = relmods.TimeFrame.objects.create(
                deadline=datetime.datetime(2021, 2, 5, tzinfo=sgtz))
        elif supply_type == SupplyAvailabilityOption.PRE_ORDER_DURATION:
            pre_order_timeframe = relmods.TimeFrame.objects.create(
                duration_uom='d',
                duration=5
            )

        # Supply
        supply = relmods.Supply.objects.create(
            user=self.user if not buying else self.user_2,
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            availability=availability,
            pre_order_timeframe=pre_order_timeframe,
            quantity=12000,
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1), # USD
            deposit_percentage=0.4,
            accept_lc=False
        )

        # Demand
        demand = relmods.Demand.objects.create(
            user=self.user if buying else self.user_2,
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            quantity=12000,
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1) # USD
        )

        # Set up match
        self.match = relmods.Match.objects.create(
            supply=supply,
            demand=demand,
            closed=datetime.datetime.now(tz=pytz.timezone(TIME_ZONE)) \
                if closed else None
        )

        # Set up user's current_match
        self.user.current_match = self.match
        self.user.save()

        return self.match

    def setup_payment_hash(self) -> paymods.PaymentHash:
        """Set up payment hash for this user and match"""
        usd = paymods.Currency.objects.get(pk=1)
        self.payment_hash = paymods.PaymentHash.objects.create(
            user=self.user,
            match=self.match,
            currency=usd,
            unit_amount=5.67
        )

        return self.payment_hash

    def setup_qna(
            self,
            answering: bool = True,
            answered: bool = False
        ) -> relmods.QuestionAnswerPair:
        """Set up QNA model and associated data key/value for this user, user_2
        and match.
        
        Parameters
        ----------
        answering
            True if this user is answering the Q&A, False otherwise.
        answered
            True if Q&A is answered, False otherwise.
        
        Returns
        -------
        Q&A model reference set up
        """

        # Dataset/value for question
        qns_ds = models.MessageDataset.objects.create(
            intent_key=intents.QNA,
            message_key=messages.QUESTION
        )
        qns_dv = models.MessageDataValue.objects.create(
            dataset=qns_ds,
            value_string='Can you do OEM?'
        )

        # Dataset/value for answer
        if answered:
            ans_ds = models.MessageDataset.objects.create(
                intent_key=intents.QNA,
                message_key=messages.ANSWER
            )
            ans_dv = models.MessageDataValue.objects.create(
                dataset=ans_ds,
                value_string='Yes, we can.'
            )
        else:
            ans_dv = None

        # Question/answer pair
        sgtz = pytz.timezone(TIME_ZONE)
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.user_2 if answering else self.user,
            answerer=self.user if answering else self.user_2,
            question_captured_value=qns_dv,
            answer_captured_value=ans_dv,
            manual_cleaned_question='Can you do OEM?',
            asked=datetime.datetime.now(tz=sgtz),
            manual_cleaned_answer='Yes, we can.' if answered else None,
            answered=datetime.datetime.now(tz=sgtz) if answered else None,
            match=self.match
        )

        # Set up user's current_qna
        self.user.current_qna = qna
        self.user.save()

        return qna

    ##### Actions #####

    def get_message(
            self,
            intent_key: str,
            message_key: str,
            inbound: bool = True
        ):
        """Returns message previously set up via its context (i.e.,
        intent_key/message_key).

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
        return views.reply(message)