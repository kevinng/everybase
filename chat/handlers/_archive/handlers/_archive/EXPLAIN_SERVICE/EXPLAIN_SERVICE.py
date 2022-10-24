from chat.libraries.sub_classes.message_handlers.menu_handler import MenuHandler

class Handler(MenuHandler):
    """We're extending menu handler even though we're not presenting the last
    option - which leads to this page"""
    pass