# Generated by Django 3.1.2 on 2021-05-25 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0064_auto_20210516_0155'),
        ('chat', '0028_auto_20210525_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontext',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('STOP_DISCUSSION', 'STOP_DISCUSSION'), ('CONNECT', 'CONNECT')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND', 'DO_NOT_UNDERSTAND'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE', 'SUPPLY__GET_COUNTRY_STATE'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY', 'SUPPLY__GET_QUANTITY'), ('SUPPLY__GET_TIMEFRAME', 'SUPPLY__GET_TIMEFRAME'), ('SUPPLY__GET_PRICE', 'SUPPLY__GET_PRICE'), ('SUPPLY__GET_DEPOSIT', 'SUPPLY__GET_DEPOSIT'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY', 'DEMAND__GET_QUANTITY'), ('DEMAND__GET_PRICE', 'DEMAND__GET_PRICE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('DISCUSS__CONFIRM_INTERESTED', 'DISCUSS__CONFIRM_INTERESTED'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_UPDATED', 'DISCUSS__CONFIRM_UPDATED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('ALREADY_CONNECTED', 'ALREADY_CONNECTED'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('STOP_DISCUSSION__REASON', 'STOP_DISCUSSION__REASON'), ('STOP_DISCUSSION__THANK_YOU', 'STOP_DISCUSSION__THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('PAYEE_CONNECTED', 'PAYEE_CONNECTED'), ('NON_PAYEE_CONNECTED', 'NON_PAYEE_CONNECTED')], db_index=True, max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='usercontext',
            unique_together={('user', 'intent_key', 'message_key')},
        ),
    ]