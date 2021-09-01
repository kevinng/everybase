from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class DiscussConfirmDetailsParameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        buying = logic.is_buying()
        match = logic.get_match()

        params = {
            'buying': buying,
            # We flip the buying flag to show self's lead details instead of
            # the counter-party's.
            'flipped_buying': not buying
        } 

        if buying:
            params['demand'] = match.demand
        else:
            params['supply'] = match.supply
        
        return params