import pytz, datetime
from everybase.settings import TIME_ZONE
from celery import shared_task
from relationships import models as relmods
from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.get_chatbot import get_chatbot
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.done_to_context import done_to_context

@shared_task
def forward_question(
        qna_id: int,
        no_external_calls: bool = False
    ):
    """Forward question to answerer

    Parameters
    ----------
    qna_id
        ID of the Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    Twilio outbound message sent
    """
    qna = relmods.QuestionAnswerPair.objects.get(pk=qna_id)

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

    # Update timestamps
    sgtz = pytz.timezone(TIME_ZONE)
    qna.question_forwarded = datetime.datetime.now(tz=sgtz)
    qna.save()

    # Update user's context
    user = qna.match.demand.user if buying else qna.match.supply.user
    done_to_context(user, intents.QNA, messages.YOUR_QUESTION)

    # Update user's current Q&A
    user.current_qna = qna
    user.save()

    return send_message(
        render_message(messages.YOUR_QUESTION, params),
        get_chatbot().phone_number,
        qna.answerer.phone_number,
        intents.QNA,
        messages.YOUR_QUESTION,
        None,
        no_external_calls
    )
