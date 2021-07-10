from chat.tasks.forward_answer import forward_answer
from urllib.parse import urljoin
from django.urls import reverse

from everybase import settings

from relationships import models as relmods

from chat.libraries.classes.message_handler_test import MessageHandlerTest
from chat.libraries.constants import intents, messages

from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption
from chat.tasks.exchange_contacts import exchange_contacts

class TasksForwardAnswerTest(MessageHandlerTest):
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
        msg = forward_answer(qna, True)
        self.assertEqual(msg, None)

    def test_run_selling(self):
        self.setup_match(False, SupplyAvailabilityOption.OTG)

        # answering=False because I'm asking the question (as a seller), so I'm
        # being forwarded (i.e., receiving) the message.
        qna = self.setup_qna(
            answering=False,
            answered=True,
            answer_readied=True
        )

        msg = forward_answer(qna, True)

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
        self.assertNotEqual(
            qna.question_forwarded,
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

        msg = forward_answer(qna, True)

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
        self.assertNotEqual(
            qna.question_forwarded,
            None
        )