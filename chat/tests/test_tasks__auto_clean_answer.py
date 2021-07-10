from chat.libraries.classes.message_handler_test import MessageHandlerTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption
from chat.tasks.auto_clean_answer import auto_clean_answer

class TasksAutoCleanAnswerTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def test_run(self):
        # Set up models
        self.setup_match(True, SupplyAvailabilityOption.OTG)
        qna = self.setup_qna(
            answered=True,
            answer_captured=\
                'My email is kevin@everybase.co and friend@everybase.co'
        )
        
        # Run task
        auto_clean_answer(qna, True)

        # Assert
        self.assertEqual(
            qna.auto_cleaned_answer,
            'My email is * and *'
        )
        self.assertEqual(
            qna.auto_cleaned_answer_w_mark_up,
            'My email is <email>kevin@everybase.co</email>\
 and <email>friend@everybase.co</email>'
        )