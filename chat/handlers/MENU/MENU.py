from chat.libraries.constants import datas
from chat.libraries.classes.menu_handler import MenuHandler

class Handler(MenuHandler):
    def __init__(self, message, intent_key, message_key):
        super().__init__(message, intent_key, message_key,
        datas.MENU__MENU__OPTION__INVALID_CHOICE__STRING)