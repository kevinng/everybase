# from chat.tests import utils
# from chat.libraries import intents, messages, datas, context_utils

# class NewSupplyGetDepositTestCase(utils.ChatFlowTest):
#     def setUp(self):
#         super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_DEPOSIT)

#     def test_enter_product(self):
#         input = '40'
#         self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
#         self.assert_value(
#             datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
#             input
#         )