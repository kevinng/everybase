from chat.constants import intents, messages
from chat.tests.library import ChatTest

class ContactRequestTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.CONTACT_REQUEST, 
            messages.CONTACT_REQUEST__CONFIRM
        )

    #TODO: we need to implement the task that sends out the initial message

    def test_enter_yes(self):
        pass
        # self.receive_reply_assert(
        #     'yes',
        #     intents.REGISTER,
        #     messages.REGISTER__CONFIRMED
        # )

    def test_enter_unrecognized_input(self):
        pass
        # self.receive_reply_assert(
        #     'huh',
        #     intents.REGISTER,
        #     messages.REGISTER__CONFIRM,
        #     target_body_message_key=messages.REGISTER__DO_NOT_UNDERSTAND
        # )