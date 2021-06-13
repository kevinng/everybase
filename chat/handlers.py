"""This file defines all ContextHandler sub-classes - i.e., actual
implementation of what to do in each context.

Classes are named in the format:

<intent key>__<message key>
"""

from chat import models
from relationships import models as relmods
from chat.libraries import (intents, messages, datas, model_utils)
from chat.libraries.message_handler import MessageHandler
from relationships import models as relmods

class SPEAK_HUMAN__CONFIRM_HUMAN(MessageHandler):
    def run(self):
        pass

class EXPLAIN_SERVICE__EXPLAIN_SERVICE(MessageHandler):
    def run(self):
        pass

# REGISTER intent

class REGISTER__REGISTER__GET_NAME(MessageHandler):
    def run(self):
        # Store message body as user's name
        user = self.message.from_user
        user.name = self.message.body.strip()
        user.save()
        
        # Menu
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})

# Menu intent

class MenuHandler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('find buyers', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_BUYER
        )
        self.add_option([('2', 0), ('find sellers', 3)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_SELLER
        )
        self.add_option([('3', 0)],
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__LEARN_MORE
        )
        return self.reply_option()

class MENU__MENU(MenuHandler):
    pass

# DISCUSS_W_BUYER intent

class DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG(MessageHandler):
    def run(self):
        pass

class DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PACKING(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING(
    MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING(
    MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PRE_ORDER(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING(
    MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING(
    MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_PRICE_PRE_ORDER(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT(MessageHandler):
    pass

class DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC(MessageHandler):
    pass

class DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM(MessageHandler):
    pass

class DISCUSS_W_BUYER__STILL_INTERESTED__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__ASK(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__THANK_YOU(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST(MessageHandler):
    pass

class DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS(MessageHandler):
    pass

# NEW_SUPPLY intent

class NEW_SUPPLY__SUPPLY__GET_PRODUCT(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING)
        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY
        )

class NEW_SUPPLY__SUPPLY__GET_AVAILABILITY(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('otg', 0), ('ready', 1)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            None,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )
        self.add_option([('2', 0), ('pre order', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            None,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )
        return self.reply_option()

class GetCountryStateBaseHandler(MessageHandler):
    def _run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING)

        # Get TOP unit of measure for product type matching the latest data
        # value string of this user with the given keys. UOM is None if user's
        # input does not match any product type.
        _, uom = self.get_product_type(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is not None:
            # UOM found, confirm packing details
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__CONFIRM_PACKING,
                params={'packing_description': uom.description}
            )
        else:
            # UOM not found, request packing details
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PACKING
            )

class NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG(
    GetCountryStateBaseHandler):
    def run(self):
        # Use base handler's logic
        return self._run()

class NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER(
    GetCountryStateBaseHandler):
    def run(self):
        # Use base handler's logic
        return self._run()

class NEW_SUPPLY__SUPPLY__CONFIRM_PACKING(MessageHandler):
    def _get_yes_message_key(self):
        # Get latest availability choice entered by user in context
        availability = self.get_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE
        ).value_string

        if availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG:
            # Goods are ready/OTG, get quantity of known packing

            _, uom = self.get_product_type(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_PRODUCT,
                datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
            )

            if uom is not None:
                # Product type and packing is known
                return messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
            else:
                # Product type and packing is not known
                return messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING

        elif availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER:
            # Goods are pre-order, get quantity and timeframe
            return messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        
        return None

    def _get_yes_params(self):
        _, uom = self.get_product_type(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is None:
            return {}

        return {
            'packing_plural' : uom.plural_name
        }

    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.NEW_SUPPLY, 
            None,
            self._get_yes_params,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES,
            None,
            self._get_yes_message_key
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PACKING,
            None,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO
        )
        return self.reply_option()

class NEW_SUPPLY__SUPPLY__GET_PACKING(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING)
        
        # Get latest availability choice entered by user in context
        availability = self.get_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE
        ).value_string

        if availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG:
            # Goods are ready/OTG, get quantity of unknown packing
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
            )
        elif availability == \
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER:
            # Goods are pre-order, get quantity and timeframe
            return self.done_reply(
                intents.NEW_SUPPLY,
                messages.SUPPLY__GET_QUANTITY_PRE_ORDER
            )

class NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
    NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING)

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )

class NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING)

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING
        )

class NEW_SUPPLY__SUPPLY__GET_QUANTITY_PRE_ORDER(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING)

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_PRE_ORDER
        )

class NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
        NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING)

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )

class NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
        NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING)

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )

class NEW_SUPPLY__SUPPLY__GET_PRICE_PRE_ORDER(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING)

        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_DEPOSIT
        )

class NEW_SUPPLY__SUPPLY__GET_DEPOSIT(MessageHandler):
    def run(self):
        # Save user input, deposit is None if value cannot be converted from
        # string to float
        deposit = self.save_body_as_float(
            datas.NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER)

        if deposit is None:
            # User input is invalid
            return self.reply_invalid_number()
        
        return self.done_reply(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_ACCEPT_LC
        )

class NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU, None,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU, None,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO
        )
        return self.reply_option()

class NEW_SUPPLY__SUPPLY__THANK_YOU(MenuHandler):
    pass

# NEW_DEMAND intent

class NEW_DEMAND__DEMAND__GET_PRODUCT(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING)

        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE
        )

class NEW_DEMAND__DEMAND__GET_COUNTRY_STATE(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING)

        # Get TOP unit of measure for product type matching the latest data
        # value string of this user with the given keys. UOM is None if user's
        # input does not match any product type.
        _, uom = self.get_product_type(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

        if uom is not None:
            # UOM found, confirm packing details
            return self.done_reply(
                intents.NEW_DEMAND,
                messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE,
                params={
                    'packing_description': uom.description,
                    'packing_plural': uom.plural_name
                }
            )
        else:
            # UOM not found, request packing details
            return self.done_reply(
                intents.NEW_DEMAND,
                messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
            )

class NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE(MessageHandler):
    def run(self):
        # Save user input, quantity is None if value cannot be converted from
        # string to float
        quantity = self.save_body_as_float(datas.\
        NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER)

        if quantity is None:
            # User input is invalid
            return self.reply_invalid_number()
        
        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )

class NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
        NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING)

        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE
        )

class NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING)

        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )

class NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE__PRICE__STRING)

        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )

class NEW_DEMAND__DEMAND__THANK_YOU(MenuHandler):
    pass


# DISCUSS_W_SELLER intent

class DISCUSS_W_SELLER__DEMAND__GET_PRODUCT(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE(
    MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE(MessageHandler):
    pass

class DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST(MessageHandler):
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
        demand_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID,
            False
        ).value_id
        demand = relmods.Demand.objects.get(pk=demand_id)
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

        supply_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID,
            False
        ).value_id
        supply = relmods.Supply.objects.get(pk=supply_id)

        return {
            'buying': True,
            'contact': contact,
            'supply': supply
        }

    def _get_no_params(self):
        """Get template parameters for no outcome
        """
        demand_id = self.get_latest_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID,
            False
        ).value_id
        demand = relmods.Demand.objects.get(pk=demand_id)
        return {
            'demand': demand
        }

    def run(self):
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

class DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU, None,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__CHOICE,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU, None,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__CHOICE,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__NO
        )
        return self.reply_option()

class DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('find buyers', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT, None,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__CHOICE,
        datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__FIND_BUYER
        )
        self.add_option([('2', 0), ('find sellers', 3)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT, None,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__CHOICE,
        datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__FIND_SELLER
        )
        self.add_option([('3', 0)],
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE, None,
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__CHOICE,
        datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__LEARN_MORE
        )
        return self.reply_option()

class DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS(MessageHandler):
    def _get_discuss_ask_params(self):
        return {'buying': True}

    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ASK, self._get_discuss_ask_params,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__CHOICE,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE, None,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__CHOICE,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__NO
        )
        return self.reply_option()

class DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED(MessageHandler):
    def run(self):
        user = relmods.User.objects.get(pk=self.message.from_user.id)
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})

class DISCUSS_W_SELLER__DISCUSS__ASK(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            DISCUSS_W_SELLER__DISCUSS__ASK__QUESTION__STRING)

        return self.done_reply(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__THANK_YOU
        )

class DISCUSS_W_SELLER__DISCUSS__THANK_YOU(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('find buyers', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_BUYER
        )
        self.add_option([('2', 0), ('find sellers', 3)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_SELLER
        )
        self.add_option([('3', 0)],
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__LEARN_MORE
        )

        user = relmods.User.objects.get(pk=self.message.from_user.id)
        return self.reply_option(
            intents.MENU, messages.MENU, {'name': user.name})

# Q&A intent

class QNA__YOUR_QUESTION(MessageHandler):
    pass

class QNA__YOUR_ANSWER(MessageHandler):
    pass

class QNA__QUESTION(MessageHandler):
    pass

class QNA__QUESTION_THANK_YOU(MessageHandler):
    pass

class QNA__ANSWER(MessageHandler):
    pass

class QNA__ANSWER_THANK_YOU(MessageHandler):
    pass

class QNA__STOP_DISCUSSION_REASON(MessageHandler):
    pass

class QNA__STOP_DISCUSSION__STOP_DISCUSSION__THANK_YOU(MessageHandler):
    pass

# CONNECT intent

class CONNECT__PLEASE_PAY(MessageHandler):
    pass

class CONNECT__CONNECTED(MessageHandler):
    pass

# No intent

class NO_INTENT__NO_MESSAGE(MessageHandler):
    def run(self):
        user = relmods.User.objects.get(pk=self.message.from_user.id)

        if user.name is None:
            # User's name not set - register him/her
            return self.done_reply(
                intents.REGISTER, messages.REGISTER__GET_NAME)

        # No active context - menu
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})