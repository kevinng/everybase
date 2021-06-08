from chat.tests import utils
from chat.libraries import intents, messages, datas
from relationships import models as relmods

class DemandConfirmInterestTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_SELLER, messages.DISCUSS__CONFIRM_INTEREST, None)
        pt, _, _ = self.set_up_known_product_type()
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__PRODUCT_TYPE__ID,
            value_id=pt.id
        )
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__USER_1__ID,
            value_id=self.user.id
        )
        self.user_2, _ = self.create_user_phone_number('Test Seller', '23456',
            '2345678901')
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__USER_2__ID,
            value_id=self.user_2.id
        )

class DemandConfirmInterest_NotConnected_Test(DemandConfirmInterestTest):
    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('10', intents.DISCUSS_W_SELLER, messages.DISCUSS__CONFIRM_INTEREST)

    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('hello', intents.DISCUSS_W_SELLER, messages.DISCUSS__CONFIRM_INTEREST)

    def test_choose_no_with_number(self):
        pass

    def test_choose_no_with_text(self):
        pass

    def test_choose_yes_with_number(self):
        pass

    def test_choose_yes_with_text(self):
        pass

    # def test_choose_yes_with_number(self):
    #     self.receive_reply_assert('1',
    #         intents.DISCUSS_W_SELLER,
    #         messages.DISCUSS__CONFIRM_INTEREST
    #     )
    #     self.assert_value(
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__CHOICE,
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__YES
    #     )

    # def test_choose_yes_with_text(self):
    #     self.receive_reply_assert('yes',
    #         intents.DISCUSS_W_SELLER,
    #         messages.DISCUSS__CONFIRM_INTEREST
    #     )
    #     self.assert_value(
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__CHOICE,
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__YES
    #     )

    # def test_choose_no_with_number(self):
    #     self.receive_reply_assert('2',
    #         intents.DISCUSS_W_SELLER,
    #         messages.DISCUSS__CONFIRM_INTEREST
    #     )
    #     self.assert_value(
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__CHOICE,
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__NO
    #     )

    # def test_choose_no_with_text(self):
    #     self.receive_reply_assert('no',
    #         intents.DISCUSS_W_SELLER,
    #         messages.DISCUSS__CONFIRM_INTEREST
    #     )
    #     self.assert_value(
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__CHOICE,
    #         datas.DISCUSS_W_SELLER__CONFIRM_INTEREST__INTERESTED__NO
    #     )

class DemandConfirmInterest_Connected_Test(DemandConfirmInterestTest):
    def setUp(self):
        super().setUp()

        # Connect users
        if self.user.id < self.user_2.id:
            user_x = self.user
            user_y = self.user_2
        else:
            user_x = self.user_2
            user_y = self.user

        connection = relmods.Connection.objects.create(
            user_1=user_x,
            user_2=user_y
        )
        self.models_to_tear_down.append(connection)

    def test_choose_yes_with_number(self):
        pass

    def test_choose_yes_with_text(self):
        pass