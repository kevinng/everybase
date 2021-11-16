from amplitude.constants import events
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.send_event(events.ENTERED_STRAY_TEXT)

        # Use render message to return message
        # return render_message(message_key, params)
        # e.g., return 'hello world'

        # An unregistered user will also come to No-Intent/No-Message because
        # the user created from this interaction will not match the user
        # that was created on the site. So, even though we've changed the
        # context of the user registered on the site to, say,
        # Register/Register-Confirm, the user will not be in this context
        # until registration is completed.
        return None