from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        """
        If the user is the answerer of the Q&A:
          - If the user has answered the question, reply answer/thank-you
              with initial=False flag.
          - If the user has not answered the question, reply your-question
        
        If the user is the questioner of the Q&A:
          - If the counter-party has answered the question, reply your-answer
          - If the country-party has not answered the question, reply
              question/thank-you with initial=False flag.
        
        User will not be allowed to ask questions if he has unanswered
        questions.
        
        The user may ask multiple questions.
        
        A user may have only one Q&A in discussion at one time.
        """
        if ContextLogic(self).get_match().closed is not None:
            return self.done_reply(intents.MENU, messages.MENU)

        self.save_body_as_string(datas.STRAY_INPUT)
        logic = ContextLogic(self)
        if logic.is_answering():
            if logic.is_answered():
                self.params['initial'] = False
                return self.done_reply(intents.QNA, messages.QNA__THANK_YOU)
            else:
                return self.done_reply(intents.QNA, messages.YOUR_QUESTION)
        elif not logic.is_answering():
            if logic.is_answered():
                return self.done_reply(intents.QNA, messages.YOUR_ANSWER)
            else:
                self.params['initial'] = False
                return self.done_reply(intents.QNA, messages.QNA__THANK_YOU)

        return None