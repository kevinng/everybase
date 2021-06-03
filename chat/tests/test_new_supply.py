from chat import models
from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils
from relationships import models as relmods
from common import models as commods

class ChooseNewSupplyTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.MENU, messages.MENU)

    def test_choose_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_choose_with_text(self):
        self.receive_reply_assert('buyer', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

class GetProductTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )

class GetAvailabilityTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
    
    def test_choose_ready_otg_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_ready_otg_with_text_1(self):
        self.receive_reply_assert('ready', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_ready_otg_with_text_2(self):
        self.receive_reply_assert('otg', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_preorder_with_number(self):
        self.receive_reply_assert('2', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_choose_preorder_with_text(self):
        self.receive_reply_assert('pre order', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

class GetCountryStateTest():
    def set_up_user_product_type_entry(self):
        # Create dummy inbound message
        msg = models.TwilioInboundMessage.objects.create()
        self.models_to_tear_down.append(msg)

        # User previously entered product type matching keyword
        ds = models.MessageDataset.objects.create(
            intent_key=intents.NEW_SUPPLY,
            message_key=messages.SUPPLY__GET_PRODUCT,
            message=msg
        )
        self.models_to_tear_down.append(ds)
        dv = models.MessageDataValue.objects.create(
            dataset=ds,
            value_string='exists',
            data_key=datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )
        self.models_to_tear_down.append(dv)
        
class GetCountryStateReadyOTGProductFoundTest(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)

        # Create test product type
        pt = relmods.ProductType.objects.create(
            name='Product That Exists'
        )
        self.models_to_tear_down.append(pt)

        # Create test unit-of-measure - required to ascertain if product type is found
        uom = relmods.UnitOfMeasure.objects.create(
            name='ProductThatExists UOM',
            description='ProductThatExists UOM',
            product_type=pt
        )
        self.models_to_tear_down.append(uom)

        # Create match keyword for test product type
        kw = commods.MatchKeyword.objects.create(
            keyword='exists',
            tolerance=0,
            product_type=pt
        )
        self.models_to_tear_down.append(kw)

        self.set_up_user_product_type_entry()

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

class GetCountryStatePreOrderTest(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_user_product_type_entry()

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)