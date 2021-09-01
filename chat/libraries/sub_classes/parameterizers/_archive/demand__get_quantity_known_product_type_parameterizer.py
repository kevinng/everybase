from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class DemandGetQuantityKnownProductTypeParameterizer(MessageParameterizer):
    def run(self) -> dict:
        _, uom = ContextLogic(self.message_handler).get_product_type()
        return {
            'packing_description': uom.description,
            'packing_plural': uom.plural_name }