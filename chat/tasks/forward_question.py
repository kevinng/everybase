from celery import shared_task
from relationships import models as relmods
from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.get_chatbot import get_chatbot
from chat.libraries.utility_funcs.render_message import render_message

@shared_task
def forward_question(
        qna: relmods.QuestionAnswerPair,
        no_external_calls: bool = False
    ):
    """Forward question to answerer

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
    if qna.question_ready is None:
        return None

    if qna.use_auto_cleaned_question is not None and \
        qna.use_auto_cleaned_question == True:
        body = qna.auto_cleaned_question
    else:
        body = qna.manual_cleaned_question

    buying = qna.match.demand.user == qna.answerer
    
    params = {
        'name': qna.answerer.name,
        'question': body,
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
        messages.YOUR_QUESTION,
        None,
        no_external_calls
    )
