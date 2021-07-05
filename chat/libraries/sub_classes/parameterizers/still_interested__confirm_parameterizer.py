from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class StillInterestedConfirmParameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        
        buying = logic.is_buying()
        params = { 'buying': buying }
        if buying:
            params['demand'] = logic.get_match().demand
        else:
            params['supply'] = logic.get_match().supply

        return params