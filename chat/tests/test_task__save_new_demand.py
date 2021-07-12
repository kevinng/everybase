from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.constants import intents, messages, datas
from chat.tasks.save_new_demand import save_new_demand

class TaskSaveNewDemandTest_ProductTypeFound(ChatTest):
    fixtures = [
        'setup/20210527__relationships__producttype.json',
        'setup/20210712__common__matchkeywords.json'
    ]

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

        msg = self.setup_inbound_message(
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )
        dmd = save_new_demand(msg)

        # Product type
        #   Data value set
        self.assertEqual(
            dmd.product_type_data_value.id,
            ptype_dv.id
        )
        #   Right product type
        self.assertEqual(
            dmd.product_type.id,
            1 # Nitrile gloves
        )
        
        # Country
        #   Data value set
        self.assertEqual(
            dmd.country_data_value.id,
            country_dv.id
        )
        #   Right country
        self.assertEqual(
            dmd.country.id,
            696 # Singapore
        )

        # Quantity
        self.assertEqual(
            dmd.quantity_data_value.id,
            quantity_dv
        )

        # Price
        self.assertEqual(
            dmd.price_data_value.id,
            price_dv
        )

# class TasksSaveNewDemandTest_ProductTypeNotFound(ChatTest):
#     fixtures = [
#         'setup/20210527__relationships__producttype.json',
#         'setup/common__country.json'
#     ]

#     def setUp(self):
#         super().setUp()

#         # A product NOT in our database
#         self.setup_data_value(
#             intents.NEW_DEMAND,
#             messages.DEMAND__GET_PRODUCT,
#             datas.PRODUCT,
#             'Chicken Nuggets'
#         )

#         self.setup_data_value(
#             intents.NEW_DEMAND,
#             messages.DEMAND__GET_COUNTRY_STATE,
#             datas.COUNTRY_STATE,
#             'Singapore'
#         )

#         # Product type found
#         self.setup_data_value(
#             intents.NEW_DEMAND,
#             messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE,
#             datas.QUANTITY,
#             '200 boxes'
#         )
#         self.setup_data_value(
#             intents.NEW_DEMAND,
#             messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE,
#             datas.PRICE,
#             'USD 5.67 per box'
#         )

#     def test_run(self):
#         pass