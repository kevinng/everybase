# Generated by Django 3.1.2 on 2021-06-04 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relationships', '0068_auto_20210527_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwilioInboundMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('api_version', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('sms_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('sms_message_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('sms_status', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('account_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message_service_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_str', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_str', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('num_media', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('num_segments', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_city', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_state', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_zip', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_country', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_city', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_state', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_zip', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_country', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('profile_name', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('wa_id', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('forwarded', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('frequently_forwarded', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('latitude', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('label', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_phone_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_from_phone_numbers', related_query_name='twilio_inbound_message_from_phone_numbers', to='relationships.phonenumber')),
                ('from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_from_users', related_query_name='twilio_inbound_message_from_users', to='relationships.user')),
                ('to_phone_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_to_phone_numbers', related_query_name='twilio_inbound_message_to_phone_numbers', to='relationships.phonenumber')),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_to_users', related_query_name='twilio_inbound_message_to_users', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwilioOutboundMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('date_created', models.DateField(blank=True, db_index=True, null=True)),
                ('date_sent', models.DateField(blank=True, db_index=True, null=True)),
                ('direction', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('account_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('from_str', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_str', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('uri', models.URLField(blank=True, db_index=True, null=True)),
                ('error_message', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('error_code', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('api_version', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwilioStatusCallback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('from_str', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('to_str', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('account_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('api_version', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('channel_to_address', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('channel_install_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('channel_status_message', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('channel_prefix', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message_status', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('sms_sid', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('sms_status', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('error_code', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('event_type', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chat.twiliooutboundmessage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('started', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('done', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('paused', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('expired', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('intent_key', models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('MENU', 'MENU'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('QNA', 'QNA'), ('CONNECT', 'CONNECT')], db_index=True, max_length=200)),
                ('message_key', models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND', 'DO_NOT_UNDERSTAND'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE_READY_OTG', 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'), ('SUPPLY__GET_COUNTRY_STATE_PRE_ORDER', 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_PRE_ORDER', 'SUPPLY__GET_QUANTITY_PRE_ORDER'), ('SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_PRICE_PRE_ORDER', 'SUPPLY__GET_PRICE_PRE_ORDER'), ('SUPPLY__GET_DEPOSIT_PRE_ORDER', 'SUPPLY__GET_DEPOSIT_PRE_ORDER'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_INTEREST', 'DISCUSS__CONFIRM_INTEREST'), ('DISCUSS__CONFIRM_DETAILS', 'DISCUSS__CONFIRM_DETAILS'), ('DISCUSS__ALREADY_CONNECTED', 'DISCUSS__ALREADY_CONNECTED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('ASK_QUESTION', 'ASK_QUESTION'), ('THANK_FOR_QUESTION', 'THANK_FOR_QUESTION'), ('REPLY', 'REPLY'), ('THANK_FOR_REPLY', 'THANK_FOR_REPLY'), ('STOP_DISCUSSION_REASON', 'STOP_DISCUSSION_REASON'), ('STOP_DISCUSSION_THANK_YOU', 'STOP_DISCUSSION_THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('CONNECTED', 'CONNECTED')], db_index=True, max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_contexts', related_query_name='user_contexts', to='relationships.user')),
            ],
            options={
                'unique_together': {('user', 'intent_key', 'message_key')},
            },
        ),
        migrations.CreateModel(
            name='TwilioStatusCallbackLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('payload', models.TextField(db_index=True)),
                ('callback', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='log_entries', related_query_name='log_entries', to='chat.twiliostatuscallback')),
            ],
            options={
                'verbose_name': 'Twilio Status Callback Log Entry',
                'verbose_name_plural': 'Twilio Status Callback Log Entries',
            },
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='context',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='twilio_outbound_messages', related_query_name='twilio_outbound_messages', to='chat.usercontext'),
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='from_phone_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_outbound_message_from_phone_numbers', related_query_name='twilio_outbound_message_from_phone_numbers', to='relationships.phonenumber'),
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_outbound_message_from_users', related_query_name='twilio_outbound_message_from_users', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='to_phone_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_outbound_message_to_phone_numbers', related_query_name='twilio_outbound_message_to_phone_numbers', to='relationships.phonenumber'),
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_outbound_message_to_users', related_query_name='twilio_outbound_message_to_users', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='twilml_response_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_outbound_message_responses', related_query_name='twilio_outbound_message_responses', to='chat.twilioinboundmessage'),
        ),
        migrations.CreateModel(
            name='TwilioInboundMessageMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('content_type', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('url', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medias', related_query_name='medias', to='chat.twilioinboundmessage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwilioInboundMessageLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('payload', models.TextField(db_index=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='log_entries', related_query_name='log_entries', to='chat.twilioinboundmessage')),
            ],
            options={
                'verbose_name': 'Twilio Inbound Message Log Entry',
                'verbose_name_plural': 'Twilio Inbound Message Log Entries',
            },
        ),
        migrations.CreateModel(
            name='MessageDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('intent_key', models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('MENU', 'MENU'), ('SPEAK_HUMAN', 'SPEAK_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('REGISTER', 'REGISTER'), ('NEW_SUPPLY', 'NEW_SUPPLY'), ('NEW_DEMAND', 'NEW_DEMAND'), ('DISCUSS_W_BUYER', 'DISCUSS_W_BUYER'), ('DISCUSS_W_SELLER', 'DISCUSS_W_SELLER'), ('QNA', 'QNA'), ('CONNECT', 'CONNECT')], db_index=True, max_length=200)),
                ('message_key', models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('MENU', 'MENU'), ('CONFIRM_HUMAN', 'CONFIRM_HUMAN'), ('EXPLAIN_SERVICE', 'EXPLAIN_SERVICE'), ('DO_NOT_UNDERSTAND', 'DO_NOT_UNDERSTAND'), ('REGISTER__GET_NAME', 'REGISTER__GET_NAME'), ('SUPPLY__GET_PRODUCT', 'SUPPLY__GET_PRODUCT'), ('SUPPLY__GET_AVAILABILITY', 'SUPPLY__GET_AVAILABILITY'), ('SUPPLY__GET_COUNTRY_STATE_READY_OTG', 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'), ('SUPPLY__GET_COUNTRY_STATE_PRE_ORDER', 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'), ('SUPPLY__CONFIRM_PACKING', 'SUPPLY__CONFIRM_PACKING'), ('SUPPLY__GET_PACKING', 'SUPPLY__GET_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_QUANTITY_PRE_ORDER', 'SUPPLY__GET_QUANTITY_PRE_ORDER'), ('SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'), ('SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING', 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'), ('SUPPLY__GET_PRICE_PRE_ORDER', 'SUPPLY__GET_PRICE_PRE_ORDER'), ('SUPPLY__GET_DEPOSIT_PRE_ORDER', 'SUPPLY__GET_DEPOSIT_PRE_ORDER'), ('SUPPLY__GET_ACCEPT_LC', 'SUPPLY__GET_ACCEPT_LC'), ('SUPPLY__THANK_YOU', 'SUPPLY__THANK_YOU'), ('DEMAND__GET_PRODUCT', 'DEMAND__GET_PRODUCT'), ('DEMAND__GET_COUNTRY_STATE', 'DEMAND__GET_COUNTRY_STATE'), ('DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'), ('DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE', 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'), ('DEMAND__THANK_YOU', 'DEMAND__THANK_YOU'), ('STILL_INTERESTED__CONFIRM', 'STILL_INTERESTED__CONFIRM'), ('STILL_INTERESTED__THANK_YOU', 'STILL_INTERESTED__THANK_YOU'), ('DISCUSS__CONFIRM_INTEREST', 'DISCUSS__CONFIRM_INTEREST'), ('DISCUSS__CONFIRM_DETAILS', 'DISCUSS__CONFIRM_DETAILS'), ('DISCUSS__ALREADY_CONNECTED', 'DISCUSS__ALREADY_CONNECTED'), ('DISCUSS__ASK', 'DISCUSS__ASK'), ('DISCUSS__THANK_YOU', 'DISCUSS__THANK_YOU'), ('YOUR_QUESTION', 'YOUR_QUESTION'), ('YOUR_ANSWER', 'YOUR_ANSWER'), ('ASK_QUESTION', 'ASK_QUESTION'), ('THANK_FOR_QUESTION', 'THANK_FOR_QUESTION'), ('REPLY', 'REPLY'), ('THANK_FOR_REPLY', 'THANK_FOR_REPLY'), ('STOP_DISCUSSION_REASON', 'STOP_DISCUSSION_REASON'), ('STOP_DISCUSSION_THANK_YOU', 'STOP_DISCUSSION_THANK_YOU'), ('PLEASE_PAY', 'PLEASE_PAY'), ('CONNECTED', 'CONNECTED')], db_index=True, max_length=200)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_datasets', related_query_name='message_datasets', to='chat.twilioinboundmessage')),
            ],
            options={
                'unique_together': {('intent_key', 'message_key', 'message')},
            },
        ),
        migrations.CreateModel(
            name='MessageDataValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('data_key', models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE', 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE'), ('NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG', 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG'), ('NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER', 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING', 'NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING'), ('NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING', 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING'), ('NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING', 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING'), ('NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING', 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING')], db_index=True, max_length=200)),
                ('value_string', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('value_float', models.FloatField(blank=True, db_index=True, null=True)),
                ('value_boolean', models.BooleanField(blank=True, db_index=True, null=True)),
                ('is_valid', models.BooleanField(blank=True, db_index=True, null=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='strings', related_query_name='strings', to='chat.messagedataset')),
            ],
            options={
                'unique_together': {('dataset', 'data_key')},
            },
        ),
    ]
