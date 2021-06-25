# Generated by Django 3.1.2 on 2021-06-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0100_auto_20210624_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedataset',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND_OPTION', 'DO_NOT_UNDERSTAND_OPTION'), ('DO_NOT_UNDERSTAND_NUMBER', 'DO_NOT_UNDERSTAND_NUMBER'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE_READY_OTG', 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'), ('SUPPLY__GET_COUNTRY_STATE_PRE_ORDER', 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_PRE_ORDER', 'SUPPLY__GET_QUANTITY_PRE_ORDER'), ('SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_PRICE_PRE_ORDER', 'SUPPLY__GET_PRICE_PRE_ORDER'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_INTEREST', 'DISCUSS__CONFIRM_INTEREST'), ('DISCUSS__CONFIRM_DETAILS', 'DISCUSS__CONFIRM_DETAILS'), ('DISCUSS__ALREADY_CONNECTED', 'DISCUSS__ALREADY_CONNECTED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('QUESTION', 'QUESTION'), ('QUESTION__THANK_YOU', 'QUESTION__THANK_YOU'), ('STOP_DISCUSSION__REASON', 'STOP_DISCUSSION__REASON'), ('STOP_DISCUSSION__THANK_YOU', 'STOP_DISCUSSION__THANK_YOU'), ('ANSWER', 'ANSWER'), ('ANSWER__THANK_YOU', 'ANSWER__THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('CONNECTED', 'CONNECTED')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND_OPTION', 'DO_NOT_UNDERSTAND_OPTION'), ('DO_NOT_UNDERSTAND_NUMBER', 'DO_NOT_UNDERSTAND_NUMBER'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE_READY_OTG', 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'), ('SUPPLY__GET_COUNTRY_STATE_PRE_ORDER', 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_PRE_ORDER', 'SUPPLY__GET_QUANTITY_PRE_ORDER'), ('SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_PRICE_PRE_ORDER', 'SUPPLY__GET_PRICE_PRE_ORDER'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_INTEREST', 'DISCUSS__CONFIRM_INTEREST'), ('DISCUSS__CONFIRM_DETAILS', 'DISCUSS__CONFIRM_DETAILS'), ('DISCUSS__ALREADY_CONNECTED', 'DISCUSS__ALREADY_CONNECTED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('QUESTION', 'QUESTION'), ('QUESTION__THANK_YOU', 'QUESTION__THANK_YOU'), ('STOP_DISCUSSION__REASON', 'STOP_DISCUSSION__REASON'), ('STOP_DISCUSSION__THANK_YOU', 'STOP_DISCUSSION__THANK_YOU'), ('ANSWER', 'ANSWER'), ('ANSWER__THANK_YOU', 'ANSWER__THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('CONNECTED', 'CONNECTED')], db_index=True, max_length=200),
        ),
    ]
