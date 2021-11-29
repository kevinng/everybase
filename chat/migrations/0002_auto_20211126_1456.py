# Generated by Django 3.1.2 on 2021-11-26 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relationships', '0001_initial'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontext',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_contexts', related_query_name='user_contexts', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='twiliostatuscallbacklogentry',
            name='callback',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='log_entries', related_query_name='log_entries', to='chat.twiliostatuscallback'),
        ),
        migrations.AddField(
            model_name='twiliostatuscallback',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chat.twiliooutboundmessage'),
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
        migrations.AddField(
            model_name='twilioinboundmessagemedia',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medias', related_query_name='medias', to='chat.twilioinboundmessage'),
        ),
        migrations.AddField(
            model_name='twilioinboundmessagelogentry',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='log_entries', related_query_name='log_entries', to='chat.twilioinboundmessage'),
        ),
        migrations.AddField(
            model_name='twilioinboundmessage',
            name='from_phone_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_from_phone_numbers', related_query_name='twilio_inbound_message_from_phone_numbers', to='relationships.phonenumber'),
        ),
        migrations.AddField(
            model_name='twilioinboundmessage',
            name='from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_from_users', related_query_name='twilio_inbound_message_from_users', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='twilioinboundmessage',
            name='to_phone_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_to_phone_numbers', related_query_name='twilio_inbound_message_to_phone_numbers', to='relationships.phonenumber'),
        ),
        migrations.AddField(
            model_name='twilioinboundmessage',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='twilio_inbound_message_to_users', related_query_name='twilio_inbound_message_to_users', to='relationships.user'),
        ),
        migrations.AlterUniqueTogether(
            name='usercontext',
            unique_together={('user', 'intent_key', 'message_key')},
        ),
    ]