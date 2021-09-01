from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption
from chat.tasks.auto_clean_question import auto_clean_question

class TaskAutoCleanQuestionTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def test_run(self):
        self.setup_match(True, SupplyAvailabilityOption.OTG)
        qna = self.setup_qna(
            answered=True,
            question_captured=\
                'My email is kevin@everybase.co and friend@everybase.co'
        )
        
        # Run task
        auto_clean_question(qna.id, True)

        # Assert
        qna.refresh_from_db()
        self.assertEqual(
            qna.auto_cleaned_question,
            'My email is * and *'
        )
        self.assertEqual(
            qna.auto_cleaned_question_w_mark_up,
            'My email is <email>kevin@everybase.co</email>\
 and <email>friend@everybase.co</email>'
        )