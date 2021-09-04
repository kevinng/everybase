from chat.libraries.classes.message_parameterizer import MessageParameterizer

class Parameterizer(MessageParameterizer):
    def run(self) -> dict:
        return { 'name': self.message_handler.message.from_user.name }