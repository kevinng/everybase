from celery import shared_task
from relationships import models as relmods
from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.get_chatbot import get_chatbot
from chat.libraries.utility_funcs.render_message import render_message

@shared_task
def forward_answer(
        qna: relmods.QuestionAnswerPair,
        no_external_calls: bool = False
    ):
    """Forward answer to questioner

    Parameters
    ----------
    qna
        Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    Twilio outbound message sent if successful, None otherwise.
    """
    if qna.answer_ready is None:
        return None

    # Question
    if qna.use_auto_cleaned_question is not None and \
        qna.use_auto_cleaned_question == True:
        question = qna.auto_cleaned_question
    else:
        question = qna.manual_cleaned_question

    # Answer
    if qna.use_auto_cleaned_answer is not None and \
        qna.use_auto_cleaned_answer == True:
        answer = qna.auto_cleaned_answer
    else:
        answer = qna.manual_cleaned_answer

    buying = qna.match.demand.user == qna.questioner
    
    params = {
        'name': qna.answerer.name,
        'question': question,
        'answer': answer,
        'buying': buying
    }

    if buying:
        params['supply'] = qna.match.supply
    else:
        params['demand'] = qna.match.demand

    return send_message(
        render_message(messages.YOUR_QUESTION, params),
        get_chatbot().phone_number,
        qna.answerer.phone_number,
        intents.QNA,
        messages.YOUR_ANSWER,
        None,
        no_external_calls
    )
