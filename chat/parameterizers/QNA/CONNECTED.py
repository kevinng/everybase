from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class Parameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        lead, buying = logic.get_lead()
        user = lead.user

        return {
            'buying': buying,
            'contact': user,
            'whatsapp_link': logic.get_create_whatsapp_link() }