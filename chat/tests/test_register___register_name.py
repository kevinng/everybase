from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class register__register_get_name_Test(ChatTest):
    def setUp(self):
        super().setUp(intents.REGISTER, messages.REGISTER__NAME, name=None)

    def test_enter_name(self):        
        self.receive_reply_assert(
            'Kevin Ng',
            intents.REGISTER,
            messages.REGISTER__EMAIL
        )
        self.assertEqual(self.user.name, 'Kevin Ng')


    

    # def choose_non_choice(self, input):
    #     self.receive_reply_assert(
    #         input,
    #         intents.TALK_TO_HUMAN,
    #         messages.TALK_TO_HUMAN__CONFIRM,
    #         target_body_intent_key=intents.NO_INTENT,
    #         target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
    #     )
    #     self.assert_value(
    #         datas.INVALID_CHOICE,
    #         value_string=input
    #     )

    # def test_choose_non_choice_with_number(self):
    #     self.choose_non_choice('10')

    # def test_choose_non_choice_with_text(self):
    #     self.choose_non_choice('hello world')

    # def test_find_me_buyers(self):
    #     self.receive_reply_assert(
    #         '1',
    #         intents.FIND_BUYERS,
    #         messages.GET_LEAD__LOCATION
    #     )
    #     self.assert_value(
    #         datas.MENU,
    #         value_string=datas.MENU__FIND_BUYERS
    #     )

    # def test_find_me_sellers(self):
    #     self.receive_reply_assert(
    #         '2',
    #         intents.FIND_SELLERS,
    #         messages.GET_LEAD__LOCATION
    #     )
    #     self.assert_value(
    #         datas.MENU,
    #         value_string=datas.MENU__FIND_SELLERS
    #     )

    # def test_talk_to_an_everybase_human_agent(self):
    #     self.receive_reply_assert(
    #         '3',
    #         intents.TALK_TO_HUMAN,
    #         messages.TALK_TO_HUMAN__CONFIRM
    #     )
    #     self.assert_value(
    #         datas.MENU,
    #         value_string=datas.MENU__TALK_TO_AN_EVERYBASE_AGENT
    #     )
    
    # def test_register_me(self):
    #     self.receive_reply_assert(
    #         '4',
    #         intents.REGISTER,
    #         messages.REGISTER__NAME
    #     )
    #     self.assert_value(
    #         datas.MENU,
    #         value_string=datas.MENU__REGISTER_ME
    #     )