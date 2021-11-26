# Generated by Django 3.1.2 on 2021-11-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20211126_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontext',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('DO_NOT_UNDERSTAND_OPTION', 'DO_NOT_UNDERSTAND_OPTION'), ('DO_NOT_UNDERSTAND_NUMBER', 'DO_NOT_UNDERSTAND_NUMBER'), ('DO_NOT_UNDERSTAND_EMAIL', 'DO_NOT_UNDERSTAND_EMAIL'), ('CONTACT_REQUEST__CONFIRM', 'CONTACT_REQUEST__CONFIRM'), ('CONTACT_REQUEST__CONTEXT_EXPIRED', 'CONTACT_REQUEST__CONTEXT_EXPIRED'), ('CONTACT_REQUEST__EXCHANGED_AUTHOR', 'CONTACT_REQUEST__EXCHANGED_AUTHOR'), ('CONTACT_REQUEST__EXCHANGED_CONTACTOR', 'CONTACT_REQUEST__EXCHANGED_CONTACTOR'), ('CONTACT_REQUEST__REASON_THANK_YOU', 'CONTACT_REQUEST__REASON_THANK_YOU'), ('CONTACT_REQUEST__REASON', 'CONTACT_REQUEST__REASON'), ('GENERIC', 'GENERIC'), ('LOGIN__CONFIRM', 'LOGIN__CONFIRM'), ('LOGIN__CONFIRMED', 'LOGIN__CONFIRMED'), ('LOGIN__DO_NOT_UNDERSTAND', 'LOGIN__DO_NOT_UNDERSTAND'), ('REGISTER__CONFIRM', 'REGISTER__CONFIRM'), ('REGISTER__CONFIRMED', 'REGISTER__CONFIRMED'), ('REGISTER__DO_NOT_UNDERSTAND', 'REGISTER__DO_NOT_UNDERSTAND')], db_index=True, max_length=200),
        ),
    ]
