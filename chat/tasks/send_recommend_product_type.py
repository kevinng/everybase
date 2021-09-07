
# import pytz, datetime
# from everybase.settings import TIME_ZONE
# from celery import shared_task
# from relationships import models as relmods
# from chat.libraries.constants import intents, messages
# from chat.libraries.utility_funcs.send_message import send_message
# from chat.libraries.utility_funcs.get_chatbot_phone_number import \
#     get_chatbot_phone_number
# from chat.libraries.utility_funcs.render_message import render_message
# from chat.libraries.utility_funcs.done_to_context import done_to_context

# @shared_task
# def forward_answer(
#         qna_id: int,
#         no_external_calls: bool = False
#     ):
#     """Forward answer to questioner

#     Parameters
#     ----------
#     qna_id
#         ID of the Q&A pair which we're working on
#     no_external_calls
#         If True, will not make external API calls - e.g., send Twilio WhatsApp
#         messages. Useful for automated testing, to ascertain model updates are
#         made correctly.

#     Returns
#     -------
#     Twilio outbound message sent
#     """
#     qna = relmods.QuestionAnswerPair.objects.get(pk=qna_id)

#     if qna.answer_ready is None:
#         return None

#     # Question
#     if qna.use_auto_cleaned_question is not None and \
#         qna.use_auto_cleaned_question == True:
#         question = qna.auto_cleaned_question
#     else:
#         question = qna.manual_cleaned_question

#     # Answer
#     if qna.use_auto_cleaned_answer is not None and \
#         qna.use_auto_cleaned_answer == True:
#         answer = qna.auto_cleaned_answer
#     else:
#         answer = qna.manual_cleaned_answer

#     buying = qna.match.demand.user == qna.questioner
    
#     params = {
#         'name': qna.questioner.name,
#         'question': question,
#         'answer': answer,
#         'buying': buying
#     }

#     # Update timestamps
#     sgtz = pytz.timezone(TIME_ZONE)
#     qna.answer_forwarded = datetime.datetime.now(tz=sgtz)
#     qna.save()

#     # Update user's context
#     user = qna.match.demand.user if buying else qna.match.supply.user
#     done_to_context(user, intents.QNA, messages.YOUR_ANSWER)

#     return send_message(
#         render_message(messages.YOUR_ANSWER, params),
#         get_chatbot_phone_number(),
#         qna.answerer.phone_number,
#         intents.QNA,
#         messages.YOUR_ANSWER,
#         None,
#         no_external_calls
#     )