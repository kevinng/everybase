from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.classes.message_parameterizer import MessageParameterizer

class Parameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        params = {
            'name': self.message_handler.message.from_user.name,
            'question': logic.get_question_text(),
            'buying': logic.is_buying()
        }

        lead, buying = logic.get_lead()
        if buying:
            params['supply'] = lead
        else:
            params['demand'] = lead

        return params