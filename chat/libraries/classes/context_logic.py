import typing

from urllib.parse import urljoin
from django.urls import reverse

from everybase import settings

from relationships import models as relmods
from payments import models as paymods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.utilities.sort_users import sort_users

class ContextLogic():
    """Business logic to a context (i.e., a unique intent/message pair).
    """
    def __init__(self, message_handler: MessageHandler) -> None:
        self.message_handler = message_handler

    ##### Supply/Demand #####

    def get_match(self) -> relmods.Match:
        """Returns current match we're confirming interest for OR discussing
        with the user"""
        return self.message_handler.message.from_user.current_match

    def get_lead(self) -> typing.Tuple[
        typing.Union[relmods.Supply, relmods.Demand], bool]:
        """Get lead - i.e., supply if user is buying, vice versa.
        
        Returns
        -------
        (lead, buying)
            lead is a supply if the user is buying, or demand if the user is
            selling. is_buying is True if user is buying, vice versa.
        """
        buying = self.is_buying()
        if buying:
            return (self.get_match().supply, buying)
        
        return (self.get_match().demand, buying)

    def get_counter_party(self) -> relmods.User:
        """Returns counter-party (e.g., seller if you're the buyer)."""
        match = self.get_match()
        if match.supply.user == self.message_handler.message.from_user:
            return match.demand.user
        
        return match.demand.user

    def get_product_type(self) -> relmods.ProductType:
        if self.is_buying():
            message_key = messages.DEMAND__GET_PRODUCT
        else:
            message_key = messages.SUPPLY__GET_PRODUCT

        return self.message_handler.get_product_type(
            self.message_handler.intent_key,
            message_key,
            datas.PRODUCT)

    def get_availability(self) -> str:
        """Return availability indicated by the user for the latest supply
        entered by the user."""
        if self.is_buying():
            # Only works for seller
            return None

        return self.message_handler.get_latest_value(
            self.message_handler.intent_key,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY
        ).value_string

    def is_buying(self) -> bool:
        """Returns True is user is buying, False otherwise. Return None if we're
        not able to ascertain if the user is buying or selling.
        
        To do so, we'll first attempt to get the match the user is currently
        involved in via the get_match function.

        If it returns None, we'll then attempt to ascertain if the user is
        buying or selling from the context.
        """
        match = self.get_match()
        if match is not None:
            if match.supply.user == self.message_handler.message.from_user:
                return False
            else:
                return True
        else:
            intent_key = self.message_handler.intent_key
            if intent_key == intents.NEW_SUPPLY or \
                intent_key == intents.DISCUSS_W_BUYER:
                return False
            elif intent_key == intents.NEW_DEMAND or \
                intent_key == intents.DISCUSS_W_SELLER:
                return True
        return None

    def is_connected(self) -> bool:
        """Returns True if user is connected with the counter-party, False
        otherwise."""
        match = self.get_match()
        user_1, user_2 = sort_users(match.supply.user, match.demand.user)

        try:
            return relmods.Connection.objects.get(
                user_1=user_1.id,
                user_2=user_2.id)
        except relmods.Connection.DoesNotExist:
            pass

        return None

    def is_known_packing(self) -> bool:
        """Returns True if the latest product indicated by the user has a known
        packaging."""
        _, uom = self.get_product_type()
        return uom is not None

    def is_ready_otg(self) -> bool:
        """Returns True if the user indicated Ready/OTG for the latest supply
        entered by the user."""
        return self.get_availability() == datas.AVAILABILITY__READY_OTG

    def is_pre_order(self) -> bool:
        """Returns True if the user indicated Pre-Order for the latest supply
        entered by the user."""
        return self.get_availability() == datas.AVAILABILITY__PRE_ORDER

    ##### Payments #####

    def get_create_payment_hash(self) -> paymods.PaymentHash:
        """Get/create payment hash of the counter-party for this unique 
        match/user pair."""
        hash, _ = paymods.PaymentHash.objects.get_or_create(
            match=self.get_match().id,
            user=self.message_handler.message.from_user)
        
        return hash

    def get_create_whatsapp_link(self) -> str:
        """Get/create WhatsApp URL for the counter-party. Get/create phone
        number hash of WhatsApp-type for the user on the counter-party and
        return a formatted WhatsApp URL."""
        whatsapp = relmods.PhoneNumberType.objects.get(id=1)

        hash = relmods.PhoneNumberHash.objects.get_or_create(
            user=self.message.from_user,
            phone_number_type=whatsapp,
            phone_number=self.get_counter_party().phone_number)

        return urljoin(settings.BASE_URL,
            reverse('chat_root:whatsapp', kwargs={ 'id': hash.id }))

    ##### Q&A #####

    def get_qna(self) -> relmods.QuestionAnswerPair:
        """Get current Q&A"""
        return self.message_handler.message.from_user.current_qna

    def is_answering(self) -> bool:
        """Returns True if user is answerer of current Q&A, False otherwise.
        Returns None if user is neither the answerer/question of his current
        Q&A - which signals an error in the system."""
        qna = self.get_qna()
        user = self.message_handler.message.from_user
        if user == qna.answerer:
            return True
        elif user == qna.questioner:
            return False
        return None

    def is_answered(self) -> bool:
        """Returns True if current Q&A is answered, False otherwise"""
        return self.get_qna().answered is not None

    def get_question_text(self) -> str:
        """Returns question text according to prioritization rules. I.e.,
        use manually cleaned text unless the use_auto_cleaned_question flag is
        True."""
        qna = self.get_qna()
        return qna.manual_cleaned_question if \
            qna.use_auto_cleaned_question is None or \
            qna.use_auto_cleaned_question == False else \
            qna.auto_cleaned_question

    def get_answer_text(self) -> str:
        """Returns answer text according to prioritization rules. I.e.,
        use manually cleaned text unless the use_auto_cleaned_answer flag is
        True."""
        qna = self.get_qna()
        return qna.manual_cleaned_answer if \
            qna.use_auto_cleaned_answer is None or \
            qna.use_auto_cleaned_answer == False else \
            qna.auto_cleaned_answer