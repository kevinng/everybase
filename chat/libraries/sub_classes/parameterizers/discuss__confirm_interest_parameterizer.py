from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class DiscussConfirmInterestParameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)

        lead, buying = logic.get_lead()
        params = {
            'name': self.message_handler.message.from_user.name,
            'buying': buying
        }
        print(params)
        
        if buying:
            params['demand'] = lead
        else:
            params['supply'] = lead

        return params