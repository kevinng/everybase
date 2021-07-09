
from django.test import TestCase

from chat import models
from relationships import models as relmods

from chat.libraries.constants import datas, intents, messages

class TasksAutoCleanAnswerTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def _test_run(self):
        # Set up QNA
        ds = models.MessageDataset.objects.create(
            intent_key=intents.NO_INTENT, # Not required for test
            message_key=messages.NO_MESSAGE # Not required for test
        )
        dv = models.MessageDataValue.objects.create(
            dataset=ds,
            data_key=datas.NO_DATA, # Not required for test
            value_string=\
                'My email is kevin@everybase.co and friend@everybase.co'
        )
        questioner = relmods.User.objects.create()
        relmods.QuestionAnswerPair.objects.create(
            question_captured_value=dv,

        )

        # Run function
        # Test QNA params

        pass
        
        # self.receive_reply_assert(
        #     'Hi' ,
        #     intents.REGISTER,
        #     messages.REGISTER__GET_NAME
        # )
        # self.assertEqual(self.user.name, None)
        
        # self.receive_reply_assert(
        #     'Kevin Ng',
        #     intents.MENU,
        #     messages.MENU
        # )
        # self.assertEqual(self.user.name, 'Kevin Ng')