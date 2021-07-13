from everybase.settings import TIME_ZONE
import pytz, datetime
from celery import shared_task
from relationships import models as relmods
from chat.libraries.cleaning_funcs.remove_emails import remove_email

@shared_task
def auto_clean_answer(
        qna_id: int,
        no_external_calls: bool = False
    ) -> relmods.QuestionAnswerPair:
    """Auto-clean answer

    Parameters
    ----------
    qna_id
        ID of the Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.
    """

    qna = relmods.QuestionAnswerPair.objects.get(pk=qna_id)
    text = qna.answer_captured_value.value_string

    # Clean
    cleaned_text, marked_text, _ = remove_email(text)
    qna.auto_cleaned_answer = cleaned_text
    qna.auto_cleaned_answer_w_mark_up = marked_text

    sgtz = pytz.timezone(TIME_ZONE)
    qna.answer_auto_cleaned = datetime.datetime.now(tz=sgtz)

    qna.save()
    return qna