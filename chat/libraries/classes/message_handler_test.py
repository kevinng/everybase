from django.test import TestCase
from django.template.loader import render_to_string

from chat import models, views
from chat.libraries.utilities.get_latest_value import get_latest_value
from chat.libraries.utilities.get_context import get_context
from chat.libraries.utilities.start_context import start_context

from relationships import models as relmods
from payments import models as paymods
from common import models as commods

class MessageHandlerTest(TestCase):
    """Base test class for testing message handlers
    """

    def setUp(self, intent_key=None, message_key=None, name='Test User',
        country_code='12345', national_number='1234567890'):
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

        self.user, _ = self.create_user_phone_number(
            name, country_code, national_number)

        self.sys_user, _ = self.create_user_phone_number(
            'Everybase Default', '65', '88933466')

        if intent_key is not None and message_key is not None:
            start_context(self.user, intent_key, message_key)

    def tearDown(self):
        super().tearDown()

        for user in self.users:
            # Delete ALL user's contexts
            models.UserContext.objects.filter(user=user).delete()

            # Delete ALL user's data values
            models.MessageDataValue.objects.filter(dataset__user=user).delete()

            # Delete ALL user's datasets
            models.MessageDataset.objects.filter(user=user).delete()
            
            # Delete ALL user's outbound messages
            models.TwilioOutboundMessage.objects.filter(from_user=user).delete()
            models.TwilioOutboundMessage.objects.filter(to_user=user).delete()

            # Delete ALL user's inbound messages
            models.TwilioInboundMessage.objects.filter(from_user=user).delete()
            models.TwilioInboundMessage.objects.filter(to_user=user).delete()

            # Get ALL user's supplies
            supplies = relmods.Supply.objects.filter(user=user)

            # Get ALL user's demands
            demands = relmods.Demand.objects.filter(user=user)

            # Delete ALL user's phone number hashes
            relmods.PhoneNumberHash.objects.filter(user=user).delete()

            # Delete ALL user's payment hashes
            paymods.PaymentHash.objects.filter(user=user).delete()

            # Delete ALL user's QNA pairs
            relmods.QuestionAnswerPair.objects.filter(questioner=user).delete()
            relmods.QuestionAnswerPair.objects.filter(answerer=user).delete()
            
            # Delete ALL user's matches
            for supply in supplies:
                relmods.Match.objects.filter(supply=supply).delete()
            
            for demand in demands:
                relmods.Match.objects.filter(demand=demand).delete()
                
            # Delete ALL user's supplies
            supplies.delete()

            # Delete ALL user's demands
            demands.delete()

            # Delete ALL user's connections
            relmods.Connection.objects.filter(user_1=user).delete()
            relmods.Connection.objects.filter(user_2=user).delete()

            # Get ALL user's phone numbers - to be deleted after user
            phone_numbers = relmods.PhoneNumber.objects.filter(user=user)
            
            # Delete user
            user.delete()

            # Delete ALL user's phone numbers
            phone_numbers.delete()

        for keyword in self.keywords:
            keyword.delete()
        
        for uom in self.uoms:
            uom.delete()
        
        for product_type in self.product_types:
            product_type.delete()

    def create_user_phone_number(self, name='Test User', country_code='12345',
        national_number='1234567890'):
        """Create a user and his phone number

        Parameters
        ----------
        name : String
            Name of the user
        country_code : String
            Country code of the user's phone number
        national_number : String
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

    def set_inbound_message(self, intent_key, message_key, message):
        if self.inbound_messages.get(intent_key) is None:
            self.inbound_messages[intent_key] = {}
        self.inbound_messages[intent_key][message_key] = message
    
    def set_outbound_message(self, intent_key, message_key, message):
        if self.outbound_messages.get(intent_key) is None:
            self.outbound_messages[intent_key] = {}
        self.outbound_messages[intent_key][message_key] = message

    def create_inbound_message(self, intent_key, message_key, body=None):
        message = models.TwilioInboundMessage.objects.create(
            body=body,
            from_user=self.user)
        self.set_inbound_message(intent_key, message_key, message)
        return message

    def create_outbound_message(self, intent_key, message_key, body=None):
        message = models.TwilioOutboundMessage.objects.create(
            body=body,
            from_user=self.sys_user)
        self.set_outbound_message(intent_key, message_key, message)
        return message
        
    def get_message(self, intent_key, message_key, inbound=True):
        messages = self.inbound_messages if inbound else self.outbound_messages

        if messages.get(intent_key) is None:
            # Intent key found
            messages[intent_key] = {}
        elif messages[intent_key].get(message_key) is not None:
            # Both keys found - return existing message
            return messages[intent_key][message_key]

        # Either key is not found, so message is not found - create new
        messages[intent_key][message_key] = \
            self.create_inbound_message(intent_key, message_key) if inbound \
                else self.create_outbound_message(intent_key, message_key)
        
        return messages[intent_key][message_key]

    def assert_context(self, intent_key, message_key):
        """Assert user's current context with input context

        intent_key : String
            Intent key for context to assert against user's context
        message_key : String
            Message key for context to assert against user's context
        """
        user_intent_key, user_message_key = get_context(self.user)
        self.assertEqual(user_intent_key, intent_key)
        self.assertEqual(user_message_key, message_key)

    def receive_reply(self, body):
        """Receive inbound message in this context and reply with message body
        
        body : String
            Message body
        """
        message = self.create_inbound_message(
            self.intent_key,
            self.message_key,
            body
        )
        return views.reply(message)

    def receive_reply_assert(self, body, intent_key, message_key,
        target_body_intent_key=None, target_body_message_key=None,
        target_body_params_func=None, target_body_variation_key=None):
        """Receive mock message, run reply over and assert after-reply context
        and response body.

        Parameters
        ----------
        body : String
            Message body
        intent_key : String
            Intent key for after-reply context to assert against user's context.
            The target body template will be read in-context.
        message_key : String
            Message key for after-reply context to assert against user's context
            The target body template will be read in-context.
        target_body_intent_key : String
            If specified, we will use this intent key intead of intent_key to
            render the target body template.
        target_body_message_key : String
            If specified, we will use this message key instead of message_key
            to render the target body template.
        target_body_params_func : Function
            Function returning the parameters for the target body template
        target_body_variation_key : String
            Variation key of the target body template - to pick up specific
            variation of the target body template
        """
        response = self.receive_reply(body)
        # print('FULL RESPONSE')
        # print(response)

        # Render target body
        if target_body_intent_key is None:
            render_intent_key = intent_key
        else:
            render_intent_key = target_body_intent_key
        
        if target_body_message_key is None:
            render_message_key = message_key
        else:
            render_message_key = target_body_message_key

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

    def assert_latest_value(self, intent_key, message_key, data_key,
        value_string=None, value_float=None, value_boolean=None,
        value_id=None):
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

    def assert_value(self, data_key, value_string=None, value_float=None,
        value_boolean=None, value_id=None):
        """Convenience method to call assert_latest_value with this' context
        and the specified data_key.

        Parameters
        ----------
        data_key : String
            Data key for the value
        value_string : String
            String value to assert against data value's string value
        value_float : Float
            Float value to assert against data value's float value
        value_boolean : Boolean
            Boolean value to assert against data value's boolean value
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

    def set_up_data_value(self, intent_key, message_key, data_key,
        value_string=None, value_float=None, value_boolean=None, value_id=None,
        inbound=True):
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

    def set_up_product_type(self, name=None, uom_name=None,
        uom_plural_name=None, uom_description=None, keyword=None):
        """Set up mock product type and relevant models

        Returns
        -------
        (product_type, unit_of_measure, keyword) : Tuple
            Tuple of product-type, unit-of-measure, matching-keyword model
            references created
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

        # Create test product type
        product_type = relmods.ProductType.objects.create(name=name)
        self.product_types.append(product_type)

        # Create test unit-of-measure - required to ascertain if product type
        # is found
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

    def set_up_supply(self, product_type=None, country=None, availability=None,
        packing=None, quantity=None, pre_order_timeframe=None, price=None,
        currency=None, deposit_percentage=None, accept_lc=None):
        """Set up mock supply

        Returns
        -------
        Mock supply model reference
        """
        return relmods.Supply.objects.create(
            user=self.user,
            product_type=product_type,
            country=country,
            availability=availability,
            packing=packing,
            quantity=quantity,
            pre_order_timeframe=pre_order_timeframe,
            price=price,
            currency=currency,
            deposit_percentage=deposit_percentage,
            accept_lc=accept_lc
        )

    def set_up_demand(self, product_type=None, country=None,
        packing=None, quantity=None, price=None, currency=None):
        """Set up mock demand

        Returns
        -------
        Mock demand model reference
        """
        return relmods.Demand.objects.create(
            user=self.user,
            product_type=product_type,
            country=country,
            packing=packing,
            quantity=quantity,
            price=price,
            currency=currency
        )