import pytz, datetime
from everybase.settings import TIME_ZONE
from chat import models
from chat.libraries.constants import intents, messages
from relationships import models as relmods

def setup_qna(
        user_1: relmods.User,
        user_2: relmods.User,
        match: relmods.Match,
        answering: bool = True,
        answered: bool = False,
        question_captured: str = None,
        answer_captured: str = None,
        manual_cleaned_question: str = None,
        manual_cleaned_answer: str = None,
        auto_cleaned_question: str = None,
        auto_cleaned_answer: str = None,
        answer_readied: bool = None
    ) -> relmods.QuestionAnswerPair:
    """Set up QNA model and associated data key/value for user.

    Returns
    -------
    Q&A model reference set up
    """

    # Dataset/value for question
    qns_ds = models.MessageDataset.objects.create(
        intent_key=intents.QNA,
        message_key=messages.QUESTION
    )
    qns_dv = models.MessageDataValue.objects.create(
        dataset=qns_ds,
        value_string=question_captured
    )

    # Dataset/value for answer
    if answered:
        ans_ds = models.MessageDataset.objects.create(
            intent_key=intents.QNA,
            message_key=messages.ANSWER
        )
        ans_dv = models.MessageDataValue.objects.create(
            dataset=ans_ds,
            value_string=answer_captured
        )
    else:
        ans_dv = None

    # Question/answer pair
    sgtz = pytz.timezone(TIME_ZONE)
    qna = relmods.QuestionAnswerPair.objects.create(
        questioner=user_2 if answering else user_1,
        answerer=user_1 if answering else user_2,
        question_captured_value=qns_dv,
        answer_captured_value=ans_dv,
        auto_cleaned_question=auto_cleaned_question,
        manual_cleaned_question=manual_cleaned_question,
        asked=datetime.datetime.now(tz=sgtz),
        auto_cleaned_answer=auto_cleaned_answer,
        manual_cleaned_answer=manual_cleaned_answer if answered else None,
        answered=datetime.datetime.now(tz=sgtz) if answered else None,
        answer_ready=datetime.datetime.now(tz=sgtz) if answer_readied else None,
        match=match
    )

    return qna