from chat.libraries.sub_classes.message_handlers.get_lead__location_handler \
    import GetLeadLocationHandler

class Handler(GetLeadLocationHandler):
    def run(self):
        return super().run(True)