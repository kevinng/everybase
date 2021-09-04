from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class Parameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        return {
            'initial': self.message_handler.params['initial'],
            'buying': logic.is_buying(),
            'answering': logic.is_answering()
        }