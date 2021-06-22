from chat.libraries.constants.datas import NEW_DEMAND__DEMAND__THANK_YOU__INVALID_CHOICE__STRING
from chat.libraries.classes.menu_handler import MenuHandler

class Handler(MenuHandler):
    def __init__(self, message, intent_key, message_key):
        super().__init__(message, intent_key, message_key, 
        NEW_DEMAND__DEMAND__THANK_YOU__INVALID_CHOICE__STRING)