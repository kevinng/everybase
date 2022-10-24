from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class Parameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        params = {
            'name': self.message_handler.message.from_user.name,
            'question': logic.get_question_text(),
            'answer': logic.get_answer_text(),
            'buying': logic.is_buying()
        }

        lead, buying = logic.get_lead()
        if buying:
            params['supply'] = lead
        else:
            params['demand'] = lead

        return params