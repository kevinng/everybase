from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class StillInterestedConfirmParameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        
        buying = logic.is_buying()
        match = logic.get_match()
        params = { 'buying': buying }
        if buying:
            params['demand'] = match.demand
        else:
            params['supply'] = match.supply

        return params