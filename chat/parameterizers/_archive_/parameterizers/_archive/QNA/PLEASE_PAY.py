from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.utility_funcs.get_payment_link import get_payment_link

class Parameterizer(MessageParameterizer):
    def run(self) -> dict:
        logic = ContextLogic(self.message_handler)
        hash = logic.get_create_payment_hash()
        return {
            'buying': logic.is_buying(),
            'price_display_name': hash.price.display_name,
            'payment_link': get_payment_link(hash)
        }