from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class MenuRegisteredTestBase():
    fixtures = ['setup/growth__note_agenda.json']

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            self.intent_key,
            self.message_key,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.INVALID_CHOICE,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello world')

    def test_find_me_buyers(self):
        self.receive_reply_assert(
            '1',
            intents.FIND_BUYERS,
            messages.GET_LEAD__LOCATION if self.user.registered is not None \
                else messages.REGISTER__NAME
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__FIND_BUYERS
        )

    def test_find_me_sellers(self):
        self.receive_reply_assert(
            '2',
            intents.FIND_SELLERS,
            messages.GET_LEAD__LOCATION if self.user.registered is not None \
                else messages.REGISTER__NAME
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__FIND_SELLERS
        )

    def test_talk_to_an_everybase_human_agent(self):
        self.receive_reply_assert(
            '3',
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM,
            target_body_variation_key='REGISTERED'
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__TALK_TO_AN_EVERYBASE_AGENT
        )

class MenuUnregisteredTestBase(MenuRegisteredTestBase):
    def test_talk_to_an_everybase_human_agent(self):
        self.receive_reply_assert(
            '3',
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM,
            target_body_variation_key='UNREGISTERED'
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__TALK_TO_AN_EVERYBASE_AGENT
        )

    def test_register_me(self):
        self.receive_reply_assert(
            '4',
            intents.REGISTER,
            messages.REGISTER__NAME
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__REGISTER_ME
        )

class MENU___MENU___Registered___Test(MenuRegisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(intents.MENU, messages.MENU, registered=True)

class MENU___MENU___Unregistered___Test(MenuUnregisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(intents.MENU, messages.MENU, registered=False)