from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.classes.message_parameterizer import MessageParameterizer

class DiscussAlreadyConnectedParameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        buying = logic.is_buying()
        match = logic.get_match()
        params = {
            'buying': buying,
            'contact': logic.get_counter_party(),
            'whatsapp_url': logic.get_create_whatsapp_link()
        }
        if buying:
            params['supply'] = match.supply
        else:
            params['demand'] = match.demand
        
        return params