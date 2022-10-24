from urllib.parse import urljoin

from django.template.loader import render_to_string

from common.tasks import send_email

from chat.models import MessageDataValue
from growth.models import Note, NoteAgenda

from chat.libraries.classes.message_handler import MessageHandler
from everybase.settings import (EMAIL_SUP_RECEIVER_EMAIL_ADDRESSES,
    EMAIL_SUP_SENDER_EMAIL_ADDRESS, BASE_URL, ADMIN_PATH)

def talk_to_an_everybase_human_agent(message_handler: MessageHandler,
    data_value: MessageDataValue):

    agenda = NoteAgenda.objects.get(programmatic_key='talk_to_human')
    note = Note.objects.create(
        agenda=agenda,
        user=message_handler.message.from_user
    )
    
    # Send an email to support email
    et_path = lambda template: 'growth/email/' + template
    subject = render_to_string(
        et_path('human_agent_request_subject.txt'),
        { 'note_id': str(note.id) }
    )
    body = render_to_string(
        et_path('human_agent_request_body.txt'), {
            'user_id': message_handler.message.from_user.id,
            'user_name': message_handler.message.from_user.name,
            'note_url': '%s/growth/note/%d/change/' % \
                (urljoin(BASE_URL, ADMIN_PATH), note.id)
        }
    )
    send_email.delay(
        subject, body,
        EMAIL_SUP_SENDER_EMAIL_ADDRESS,
        EMAIL_SUP_RECEIVER_EMAIL_ADDRESSES,
    )