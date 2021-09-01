from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.constants import datas, intents, messages, methods
from chat.tasks.save_new_supply_version import save_new_supply_version

_fixtures = [
    'setup/20210527__relationships__availability.json',
    'setup/20210528__payments__currency.json',
    'setup/20210527__relationships__producttype.json',
    'setup/20210527__relationships__unitofmeasure.json',
    'setup/20210712__common__matchkeywords.json',
    'setup/common__country.json'
]

class TaskSaveNewSupplyVersionTest_OTG(ChatTest):
    fixtures = _fixtures

    def test_known_packing(self):
        ptype_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'Nitrile Gloves' # Known product
        )
        availability_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__READY_OTG
        )
        country_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            datas.COUNTRY_STATE,
            'Singapore'
        )
        cfmpack_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__CONFIRM_PACKING,
            datas.CONFIRM_PACKING,
            datas.CONFIRM_PACKING__YES
        )
        quantity_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING,
            datas.QUANTITY,
            '200 boxes'
        )
        price_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING,
            datas.PRICE,
            'USD 5.67 per box'
        )

        # Message concluding the sequence
        msg = self.setup_inbound_message(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK
        )

        # Match to update
        match = self.setup_match(True, SupplyAvailabilityOption.OTG)

        sup = save_new_supply_version(match.id, msg.id)

        # Product type
        self.assertEqual(sup.product_type.id, 1) # Nitrile gloves
        self.assertEqual(sup.product_type_data_value.id, ptype_dv.id)
        self.assertEqual(sup.product_type_method, methods.FREE_TEXT_INPUT)

        # Availability
        self.assertEqual(sup.availability.id, 1) # Ready/OTG
        self.assertEqual(sup.availability_data_value.id, availability_dv.id)
        self.assertEqual(sup.availability_method, methods.DATA_KEY_MATCH)

        # Country
        self.assertEqual(sup.country.id, 696) # Singapore
        self.assertEqual(sup.country_data_value.id, country_dv.id)
        self.assertEqual(sup.country_method, methods.FREE_TEXT_INPUT)

        # Confirm packing
        self.assertEqual(sup.packing.id, 1) # Nitrile gloves top UOM
        self.assertEqual(sup.packing_data_value.id, cfmpack_dv.id)
        self.assertEqual(sup.packing_method, methods.DATA_KEY_MATCH)

        # Confirm quantity
        self.assertEqual(sup.quantity_data_value.id, quantity_dv.id)
        self.assertEqual(sup.quantity_method, methods.FREE_TEXT_INPUT)

        # Confirm price
        self.assertEqual(sup.price_data_value.id, price_dv.id)
        self.assertEqual(sup.price_method, methods.FREE_TEXT_INPUT)

        # Match's supply
        match.refresh_from_db()
        self.assertEqual(sup.id, match.supply.id)

    def test_unknown_packing_country(self):
        ptype_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'Apple Juice' # Unknown product
        )
        availability_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__READY_OTG
        )
        country_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            datas.COUNTRY_STATE,
            'Wakanda' # Unknown country
        )
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__CONFIRM_PACKING,
            datas.CONFIRM_PACKING,
            datas.CONFIRM_PACKING__NO
        )
        packing_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PACKING,
            datas.PACKING,
            '100 pieces per box'
        )
        quantity_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING,
            datas.QUANTITY,
            '200 boxes'
        )
        price_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING,
            datas.PRICE,
            'USD 5.67 per box'
        )

        # Message concluding the sequence
        msg = self.setup_inbound_message(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK
        )

        # Match to update
        match = self.setup_match(True, SupplyAvailabilityOption.OTG)

        sup = save_new_supply_version(match.id, msg.id)

        # Product type
        self.assertIsNone(sup.product_type)
        self.assertEqual(sup.product_type_data_value.id, ptype_dv.id)
        self.assertEqual(sup.product_type_method, methods.FREE_TEXT_INPUT)

        # Availability
        self.assertEqual(sup.availability.id, 1) # Ready/OTG
        self.assertEqual(sup.availability_data_value.id, availability_dv.id)
        self.assertEqual(sup.availability_method, methods.DATA_KEY_MATCH)

        # Country
        self.assertIsNone(sup.country)
        self.assertEqual(sup.country_data_value.id, country_dv.id)
        self.assertEqual(sup.country_method, methods.FREE_TEXT_INPUT)

        # Confirm packing
        self.assertIsNone(sup.packing)
        self.assertEqual(sup.packing_data_value.id, packing_dv.id)
        self.assertEqual(sup.packing_method, methods.FREE_TEXT_INPUT)

        # Confirm quantity
        self.assertEqual(sup.quantity_data_value.id, quantity_dv.id)
        self.assertEqual(sup.quantity_method, methods.FREE_TEXT_INPUT)

        # Confirm price
        self.assertEqual(sup.price_data_value.id, price_dv.id)
        self.assertEqual(sup.price_method, methods.FREE_TEXT_INPUT)

        # Match's supply
        match.refresh_from_db()
        self.assertEqual(sup.id, match.supply.id)

class TaskSaveNewSupplyTest_PreOrder(ChatTest):
    fixtures = _fixtures

    def test_known_packing(self):
        ptype_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'Nitrile Gloves' # Known product
        )
        availability_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__PRE_ORDER
        )
        country_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            datas.COUNTRY_STATE,
            'Singapore' # Known country
        )
        cfmpack_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__CONFIRM_PACKING,
            datas.CONFIRM_PACKING,
            datas.CONFIRM_PACKING__YES
        )
        quantity_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER,
            datas.QUANTITY,
            '200 boxes'
        )
        price_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_PRE_ORDER,
            datas.PRICE,
            'USD 5.67 per box'
        )
        deposit_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_DEPOSIT,
            datas.DEPOSIT,
            value_float=40
        )
        accept_lc_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_ACCEPT_LC,
            datas.ACCEPT_LC,
            datas.ACCEPT_LC__YES
        )

        # Message concluding the sequence
        msg = self.setup_inbound_message(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK
        )

        # Match to update
        match = self.setup_match(True, SupplyAvailabilityOption.OTG)

        sup = save_new_supply_version(match.id, msg.id)

        # Product type
        self.assertEqual(sup.product_type.id, 1) # Nitrile gloves
        self.assertEqual(sup.product_type_data_value.id, ptype_dv.id)
        self.assertEqual(sup.product_type_method, methods.FREE_TEXT_INPUT)

        # Availability
        self.assertEqual(sup.availability.id, 2) # Pre-order
        self.assertEqual(sup.availability_data_value.id, availability_dv.id)
        self.assertEqual(sup.availability_method, methods.DATA_KEY_MATCH)

        # Country
        self.assertEqual(sup.country.id, 696) # Singapore
        self.assertEqual(sup.country_data_value.id, country_dv.id)
        self.assertEqual(sup.country_method, methods.FREE_TEXT_INPUT)

        # Confirm packing
        self.assertEqual(sup.packing.id, 1) # Nitrile gloves top UOM
        self.assertEqual(sup.packing_data_value.id, cfmpack_dv.id)
        self.assertEqual(sup.packing_method, methods.DATA_KEY_MATCH)

        # Confirm quantity
        self.assertEqual(sup.quantity_data_value.id, quantity_dv.id)
        self.assertEqual(sup.quantity_method, methods.FREE_TEXT_INPUT)

        # Confirm price
        self.assertEqual(sup.price_data_value.id, price_dv.id)
        self.assertEqual(sup.price_method, methods.FREE_TEXT_INPUT)

        # Deposit
        self.assertEqual(sup.deposit_percentage, 40)
        self.assertEqual(sup.deposit_percentage_data_value.id, deposit_dv.id)
        self.assertEqual(sup.deposit_percentage_method, methods.NUMERIC_INPUT)

        # Accept LC
        self.assertTrue(sup.accept_lc)
        self.assertEqual(sup.accept_lc_data_value.id, accept_lc_dv.id)
        self.assertEqual(sup.accept_lc_method, methods.DATA_KEY_MATCH)

        # Match's supply
        match.refresh_from_db()
        self.assertEqual(sup.id, match.supply.id)

    def test_unknown_packing_country(self):
        ptype_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'Apple Juice' # Unknown product
        )
        availability_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__PRE_ORDER
        )
        country_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            datas.COUNTRY_STATE,
            'Wakanda' # Unknown country
        )
        quantity_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER,
            datas.QUANTITY,
            '200 boxes'
        )
        price_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_PRE_ORDER,
            datas.PRICE,
            'USD 5.67 per box'
        )
        deposit_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_DEPOSIT,
            datas.DEPOSIT,
            value_float=40
        )
        accept_lc_dv = self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_ACCEPT_LC,
            datas.ACCEPT_LC,
            datas.ACCEPT_LC__YES
        )

        # Message concluding the sequence
        msg = self.setup_inbound_message(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK
        )

        # Match to update
        match = self.setup_match(True, SupplyAvailabilityOption.OTG)

        sup = save_new_supply_version(match.id, msg.id)

        # Product type
        self.assertEqual(sup.product_type, None)
        self.assertEqual(sup.product_type_data_value.id, ptype_dv.id)
        self.assertEqual(sup.product_type_method, methods.FREE_TEXT_INPUT)

        # Availability
        self.assertEqual(sup.availability.id, 2) # Pre-order
        self.assertEqual(sup.availability_data_value.id, availability_dv.id)
        self.assertEqual(sup.availability_method, methods.DATA_KEY_MATCH)

        # Country
        self.assertEqual(sup.country, None)
        self.assertEqual(sup.country_data_value.id, country_dv.id)
        self.assertEqual(sup.country_method, methods.FREE_TEXT_INPUT)

        # Confirm quantity
        self.assertEqual(sup.quantity_data_value.id, quantity_dv.id)
        self.assertEqual(sup.quantity_method, methods.FREE_TEXT_INPUT)

        # Confirm price
        self.assertEqual(sup.price_data_value.id, price_dv.id)
        self.assertEqual(sup.price_method, methods.FREE_TEXT_INPUT)

        # Deposit
        self.assertEqual(sup.deposit_percentage, 40)
        self.assertEqual(sup.deposit_percentage_data_value.id, deposit_dv.id)
        self.assertEqual(sup.deposit_percentage_method, methods.NUMERIC_INPUT)

        # Accept LC
        self.assertTrue(sup.accept_lc)
        self.assertEqual(sup.accept_lc_data_value.id, accept_lc_dv.id)
        self.assertEqual(sup.accept_lc_method, methods.DATA_KEY_MATCH)

        # Match's supply
        match.refresh_from_db()
        self.assertEqual(sup.id, match.supply.id)