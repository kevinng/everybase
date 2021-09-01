from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.constants import intents, messages

from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

from chat.tasks.forward_answer import forward_answer

class TaskForwardAnswerTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json',
        'setup/20210527__relationships__user.json',
        'setup/20210527__relationships__phonenumber.json',
        'setup/20210527__relationships__phonenumbertype.json'
    ]

    def test_answer_not_ready(self):
        self.setup_match(False, SupplyAvailabilityOption.OTG)
        qna = self.setup_qna(answer_readied=False)
        msg = forward_answer(qna.id, True)
        self.assertIsNone(msg)

    def test_run_selling(self):
        self.setup_match(False, SupplyAvailabilityOption.OTG)

        # answering=False because I'm asking the question (as a seller), so I'm
        # being forwarded (i.e., receiving) the message.
        qna = self.setup_qna(
            answering=False,
            answered=True,
            answer_readied=True
        )

        msg = forward_answer(qna.id, True)

        qna.refresh_from_db()
        self.send_assert(
            msg.body,
            intents.QNA,
            messages.YOUR_ANSWER,
            target_body_variation_key='SELLING'
        )
        self.assertNotEqual(
            qna.answer_forwarded,
            None
        )

    def test_run_buying(self):
        self.setup_match(True, SupplyAvailabilityOption.OTG)

        # answering=False because I'm asking the question (as a buyer), so I'm
        # being forwarded (i.e., receiving) the message.
        qna = self.setup_qna(
            answering=False,
            answered=True,
            answer_readied=True
        )

        msg = forward_answer(qna.id, True)

        qna.refresh_from_db()
        self.send_assert(
            msg.body,
            intents.QNA,
            messages.YOUR_ANSWER,
            target_body_variation_key='BUYING'
        )
        self.assertNotEqual(
            qna.answer_forwarded,
            None
        )