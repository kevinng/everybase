from amplitude.constants import events
from chat.libraries.constants import intents, messages
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.send_event(events.ENTERED_STRAY_TEXT)

        # Use render message to return message
        # return render_message(message_key, params)
        # e.g., return 'hello world'

        # An unregistered user will also come to No-Intent/No-Message because
        # the user created from this interaction will not match the user
        # that was created on the site. So, even though we've 
        return None
        
        # if self.message.from_user.registered is None:
        #     rpos = self.message.body.find('register')
        #     if rpos == -1:
        #         # Register keyword not found - return menu
        #         return self.done_reply(intents.MENU, messages.MENU,
        #             lambda : { 
        #                 'message': 'default',
        #                 'register': True
        #         })
        #     else:
        #         # Register keyword found - register user
        #         return self.done_reply(
        #             intents.REGISTER,
        #             messages.REGISTER__NAME
        #         )

        # return self.done_reply(intents.MENU, messages.MENU)