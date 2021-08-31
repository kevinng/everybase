# Generated by Django 3.1.2 on 2021-08-31 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0119_auto_20210830_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedataset',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('MENU', 'MENU'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('QNA', 'QNA'), ('FIND_ME_BUYERS', 'FIND_ME_BUYERS'), ('FIND_ME_SELLERS', 'FIND_ME_SELLERS'), ('TALK_TO_HUMAN', 'TALK_TO_HUMAN')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='messagedataset',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('MENU_V2', 'MENU_V2'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND_OPTION', 'DO_NOT_UNDERSTAND_OPTION'), ('DO_NOT_UNDERSTAND_NUMBER', 'DO_NOT_UNDERSTAND_NUMBER'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE_READY_OTG', 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'), ('SUPPLY__GET_COUNTRY_STATE_PRE_ORDER', 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_PRE_ORDER', 'SUPPLY__GET_QUANTITY_PRE_ORDER'), ('SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_PRICE_PRE_ORDER', 'SUPPLY__GET_PRICE_PRE_ORDER'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_INTEREST', 'DISCUSS__CONFIRM_INTEREST'), ('DISCUSS__CONFIRM_DETAILS', 'DISCUSS__CONFIRM_DETAILS'), ('DISCUSS__ALREADY_CONNECTED', 'DISCUSS__ALREADY_CONNECTED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('QUESTION', 'QUESTION'), ('STOP_DISCUSSION__REASON', 'STOP_DISCUSSION__REASON'), ('STOP_DISCUSSION__THANK_YOU', 'STOP_DISCUSSION__THANK_YOU'), ('ANSWER', 'ANSWER'), ('QNA__THANK_YOU', 'QNA__THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('CONNECTED', 'CONNECTED'), ('FIND_BUYERS__GET_LEAD_LOCATION', 'FIND_BUYERS__GET_LEAD_LOCATION'), ('FIND_SELLERS__GET_LEAD_LOCATION', 'FIND_SELLERS__GET_LEAD_LOCATION'), ('FIND_BUYERS__GET_LEAD_DETAILS', 'FIND_BUYERS__GET_LEAD_DETAILS'), ('FIND_SELLERS__GET_LEAD_DETAILS', 'FIND_SELLERS__GET_LEAD_DETAILS'), ('TALK_TO_HUMAN', 'TALK_TO_HUMAN')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('MENU', 'MENU'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('QNA', 'QNA'), ('FIND_ME_BUYERS', 'FIND_ME_BUYERS'), ('FIND_ME_SELLERS', 'FIND_ME_SELLERS'), ('TALK_TO_HUMAN', 'TALK_TO_HUMAN')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('MENU_V2', 'MENU_V2'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND_OPTION', 'DO_NOT_UNDERSTAND_OPTION'), ('DO_NOT_UNDERSTAND_NUMBER', 'DO_NOT_UNDERSTAND_NUMBER'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE_READY_OTG', 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'), ('SUPPLY__GET_COUNTRY_STATE_PRE_ORDER', 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_PRE_ORDER', 'SUPPLY__GET_QUANTITY_PRE_ORDER'), ('SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_PRICE_PRE_ORDER', 'SUPPLY__GET_PRICE_PRE_ORDER'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_INTEREST', 'DISCUSS__CONFIRM_INTEREST'), ('DISCUSS__CONFIRM_DETAILS', 'DISCUSS__CONFIRM_DETAILS'), ('DISCUSS__ALREADY_CONNECTED', 'DISCUSS__ALREADY_CONNECTED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('QUESTION', 'QUESTION'), ('STOP_DISCUSSION__REASON', 'STOP_DISCUSSION__REASON'), ('STOP_DISCUSSION__THANK_YOU', 'STOP_DISCUSSION__THANK_YOU'), ('ANSWER', 'ANSWER'), ('QNA__THANK_YOU', 'QNA__THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('CONNECTED', 'CONNECTED'), ('FIND_BUYERS__GET_LEAD_LOCATION', 'FIND_BUYERS__GET_LEAD_LOCATION'), ('FIND_SELLERS__GET_LEAD_LOCATION', 'FIND_SELLERS__GET_LEAD_LOCATION'), ('FIND_BUYERS__GET_LEAD_DETAILS', 'FIND_BUYERS__GET_LEAD_DETAILS'), ('FIND_SELLERS__GET_LEAD_DETAILS', 'FIND_SELLERS__GET_LEAD_DETAILS'), ('TALK_TO_HUMAN', 'TALK_TO_HUMAN')], db_index=True, max_length=200),
        ),
    ]
