from chat import models
from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils
from relationships import models as relmods
from common import models as commods

class GetCountryStateTest():
    def set_up_known_product_type(self):
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

        self.set_up_known_product_type()

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

class GetCountryStatePreOrderTest(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_known_product_type()

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)