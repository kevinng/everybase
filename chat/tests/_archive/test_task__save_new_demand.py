from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.constants import intents, messages, datas, methods
from chat.tasks.save_new_demand import save_new_demand

_fixtures = [
    'setup/20210527__relationships__producttype.json',
    'setup/20210527__relationships__unitofmeasure.json',
    'setup/20210712__common__matchkeywords.json',
    'setup/common__country.json'
]

class TaskSaveNewDemandTest_ProductTypeFound(ChatTest):
    fixtures = _fixtures

    def test_run(self):
        # Setup
        ptype_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.PRODUCT,
            'Nitrile Gloves' # A product in our database
        )
        country_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE,
            datas.COUNTRY_STATE,
            'Singapore'
        )
        quantity_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE,
            datas.QUANTITY,
            '200 boxes'
        )
        price_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE,
            datas.PRICE,
            'USD 5.67 per box'
        )

        # Message concluding the sequence
        msg = self.setup_inbound_message(intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU)

        dmd = save_new_demand(msg.id)

        # Product type
        self.assertEqual(dmd.product_type.id, 1) # Nitrile gloves
        self.assertEqual(dmd.product_type_data_value.id, ptype_dv.id)
        self.assertEqual(dmd.product_type_method, methods.FREE_TEXT_INPUT)
        
        # Country
        self.assertEqual(dmd.country_data_value.id, country_dv.id)
        self.assertEqual(dmd.country.id, 696) # Singapore
        self.assertEqual(dmd.country_method, methods.FREE_TEXT_INPUT)

        # Quantity
        self.assertEqual(dmd.quantity_data_value.id, quantity_dv.id)
        self.assertEqual(dmd.quantity_method, methods.FREE_TEXT_INPUT)

        # Price
        self.assertEqual(dmd.price_data_value.id, price_dv.id)
        self.assertEqual(dmd.price_method, methods.FREE_TEXT_INPUT)

class TaskSaveNewDemandTest_ProductTypeCountryNotFound(ChatTest):
    fixtures = _fixtures

    def test_run(self):
        # Setup
        ptype_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.PRODUCT,
            'Apple Juice' # A product NOT in our database
        )
        country_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE,
            datas.COUNTRY_STATE,
            'Wakanda' # A country NOT in our database
        )
        quantity_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE,
            datas.QUANTITY,
            '200 boxes'
        )
        price_dv = self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE,
            datas.PRICE,
            'USD 5.67 per box'
        )

        msg = self.setup_inbound_message(
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )

        dmd = save_new_demand(msg.id)

        # Product type
        self.assertIsNone(dmd.product_type)
        self.assertEqual(dmd.product_type_data_value.id, ptype_dv.id)
        self.assertEqual(dmd.product_type_method, methods.FREE_TEXT_INPUT)
        
        # Country
        self.assertIsNone(dmd.country)
        self.assertEqual(dmd.country_data_value.id, country_dv.id)
        self.assertEqual(dmd.country_method, methods.FREE_TEXT_INPUT)

        # Quantity
        self.assertEqual(dmd.quantity_data_value.id, quantity_dv.id)
        self.assertEqual(dmd.quantity_method, methods.FREE_TEXT_INPUT)

        # Price
        self.assertEqual(dmd.price_data_value.id, price_dv.id)
        self.assertEqual(dmd.price_method, methods.FREE_TEXT_INPUT)