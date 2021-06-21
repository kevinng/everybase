from urllib.parse import urljoin
from django.urls import reverse

from everybase import settings
from relationships import models as relmods
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def _get_match(self):
        if not hasattr(self, '_match') or self._match is None:
            match_id = self.get_latest_value(
                intents.DISCUSS_W_SELLER,
                messages.DISCUSS__CONFIRM_INTEREST,
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__MATCH_ID__ID,
                False
            ).value_id
            self._match = relmods.Match.objects.get(pk=match_id)
        
        return self._match

    def _get_connected_env_var(self):
        """Returns true if both users are connected, false otherwise.
        """
        user_1_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_1__ID,
            False
        ).value_id

        user_2_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_2__ID,
            False
        ).value_id

        try:
            connection = relmods.Connection.objects.get(
                user_1=user_1_id,
                user_2_id=user_2_id
            )
        except relmods.Connection.DoesNotExist:
            return False

        return connection is not None
        
    def _get_yes_not_connected_params(self):
        """Get template parameters for yes/not-connected outcome
        """
        demand = self._get_match().demand
        return {
            'buying': True,
            'demand': demand
        }
    
    def _get_yes_connected_params(self):
        """Get template parameters for yes/connected outcome
        """

        # Ascertain if user 1/2 is this user, then get the reference of the
        # other user

        user_1_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_1__ID,
            False
        ).value_id

        user_2_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_2__ID,
            False
        ).value_id

        if self.message.from_user.id == user_1_id:
            # User 1 is this user - pass user 2's contact
            contact_id = user_2_id
        elif self.message.from_user.id == user_2_id:
            # User 2 is this user - pass user 1's contact
            contact_id = user_1_id
        else:
            # Unlikely, but raise an error just in case
            raise Exception("User 1 and 2's ID do not match this user's ID")

        contact = relmods.User.objects.get(pk=contact_id)

        # Get supply reference
        supply = self._get_match().supply

        # Create a WhatsApp phone-number hash for this user
        whatsapp_type = relmods.PhoneNumberType.objects.get(id=1) # WhatsApp
        wa_hash = relmods.PhoneNumberHash.objects.create(
            user=self.message.from_user,
            phone_number_type=whatsapp_type,
            phone_number=contact.phone_number
        )
        whatsapp_url = urljoin(settings.BASE_URL,
            reverse('chat_root:whatsapp', kwargs={ 'id': wa_hash.id }))

        return {
            'buying': True,
            'contact': contact,
            'supply': supply,
            'whatsapp_url': whatsapp_url
        }

    def _get_no_params(self):
        """Get template parameters for no outcome
        """
        demand = self._get_match().demand
        return {
            'demand': demand
        }

    def run(self):
        if self._get_match().closed is not None:
            # Match is closed - return menu
            user = relmods.User.objects.get(pk=self.message.from_user.id)
            return self.done_reply(
                intents.MENU,
                messages.MENU,
                {'name': user.name}
            )

        # Set environment variable
        # Test if users are connected, if so, set 'CONNECTED' in this message
        # handler environment to True.
        self.set_env_var('CONNECTED', value_func=self._get_connected_env_var)
        connected = self.get_env_var('CONNECTED')

        # Set outcomes if the user selects 'yes' depending on whether the user
        # is already connected with the seller or not.
        if connected:
            yes_message_key = messages.DISCUSS__ALREADY_CONNECTED
            yes_params_func = self._get_yes_connected_params
        else:
            yes_message_key = messages.DISCUSS__CONFIRM_DETAILS
            yes_params_func = self._get_yes_not_connected_params

        self.add_option([('1', 0), ('yes', 0)],
            intents.DISCUSS_W_SELLER,
            yes_message_key,
            yes_params_func,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM,
            self._get_no_params,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO
        )
        return self.reply_option()