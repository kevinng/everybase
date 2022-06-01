# Generated by Django 3.1.2 on 2022-05-31 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_auto_20220525_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontext',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('REGISTER', 'REGISTER'), ('LOGIN', 'LOGIN'), ('LEAD', 'LEAD'), ('WELCOME', 'WELCOME'), ('CONFIRM_LOGIN', 'CONFIRM_LOGIN'), ('NEW_APPLICATION', 'NEW_APPLICATION')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='message_key',
            field=models.CharField(choices=[('NO_MESSAGE', 'NO_MESSAGE'), ('DO_NOT_UNDERSTAND_OPTION', 'DO_NOT_UNDERSTAND_OPTION'), ('DO_NOT_UNDERSTAND_NUMBER', 'DO_NOT_UNDERSTAND_NUMBER'), ('DO_NOT_UNDERSTAND_EMAIL', 'DO_NOT_UNDERSTAND_EMAIL'), ('LOGIN__AGAIN', 'LOGIN__AGAIN'), ('LOGIN__CONFIRM', 'LOGIN__CONFIRM'), ('LOGIN__CONFIRMED', 'LOGIN__CONFIRMED'), ('LOGIN__DO_NOT_UNDERSTAND', 'LOGIN__DO_NOT_UNDERSTAND'), ('REGISTER__AGAIN', 'REGISTER__AGAIN'), ('REGISTER__CONFIRM', 'REGISTER__CONFIRM'), ('REGISTER__CONFIRMED', 'REGISTER__CONFIRMED'), ('REGISTER__DO_NOT_UNDERSTAND', 'REGISTER__DO_NOT_UNDERSTAND'), ('LEAD__CREATED', 'LEAD__CREATED'), ('WELCOME', 'WELCOME'), ('CONFIRM_LOGIN', 'CONFIRM_LOGIN'), ('NEW_APPLICATION', 'NEW_APPLICATION')], db_index=True, max_length=200),
        ),
    ]
