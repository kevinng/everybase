from everybase.settings import TIME_ZONE
import pytz, datetime
from celery import shared_task
from relationships import models as relmods
from chat.libraries.cleaning_funcs.remove_emails import remove_email

@shared_task
def auto_clean_question(
        qna: relmods.QuestionAnswerPair,
        no_external_calls: bool = False
    ):
    """Auto-clean question

    Parameters
    ----------
    qna
        Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.
    """

    text = qna.question_captured_value.value_string

    # Clean
    cleaned_text, marked_text, _ = remove_email(text)
    qna.auto_cleaned_question = cleaned_text
    qna.auto_cleaned_question_w_mark_up = marked_text
    qna.save()

    sgtz = pytz.timezone(TIME_ZONE)
    qna.question_auto_cleaned = datetime.datetime.now(tz=sgtz)