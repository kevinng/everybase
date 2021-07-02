import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from chat.libraries.classes.message_handler import MessageHandler

class MessageParameterizer(ABC):
    """Returns the parameters to its associated template. This class is
    subclassed by a parameterizer of its associated template. A template has
    a system-wide message key. To faciliate the look-up and instantiation of
    a sub-classed parameterizer, a sub-class is saved in the path
    chat.parameterizers with its message key as filename. E.g.,

    chat.parameterizers.PLEASE_PAY
    chat/parameterizers/PLEASE_PAY.py

    The sub-class must be named Params. The parameterizer will be initialized
    as such. E.g.,
    
    PLEASE_PAY.Params()
    """

    def __init__(self, message_handler: 'MessageHandler') -> None:
        """
        Parameters
        ----------
        message_handler
            Associated message handler
        """
        self.message_handler = message_handler

    @abstractmethod
    def run(self) -> dict:
        """Computes and returns parameters for its associated message template.
        This method is designed to be overwrittened.

        Returns
        -------
        dict
            Parameters for associated template
        """
        return {}