from chat.libraries.constants.datas import COUNTRY_STATE
from chat.libraries.classes.message_parameterizer import MessageParameterizer
from chat.libraries.classes.context_logic import ContextLogic

class DemandGetPriceKnownProductTypeParameterizer(MessageParameterizer):
    def run(self) -> dict:
        _, uom = ContextLogic(self.message_handler).get_product_type()
        return { 'packing_single': uom.name }