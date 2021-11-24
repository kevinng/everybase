# Generated by Django 3.1.2 on 2021-11-15 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0147_auto_20211115_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedataset',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('REGISTER', 'REGISTER'), ('LOGIN', 'LOGIN'), ('CONTACT_REQUEST__CONFIRM', 'CONTACT_REQUEST__CONFIRM'), ('CONTACT_REQUEST__THANK_YOU_AUTHOR', 'CONTACT_REQUEST__THANK_YOU_AUTHOR'), ('CONTACT_REQUEST__THANK_YOU_CONTRACTOR', 'CONTACT_REQUEST__THANK_YOU_CONTRACTOR')], db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usercontext',
            name='intent_key',
            field=models.CharField(choices=[('NO_INTENT', 'NO_INTENT'), ('REGISTER', 'REGISTER'), ('LOGIN', 'LOGIN'), ('CONTACT_REQUEST__CONFIRM', 'CONTACT_REQUEST__CONFIRM'), ('CONTACT_REQUEST__THANK_YOU_AUTHOR', 'CONTACT_REQUEST__THANK_YOU_AUTHOR'), ('CONTACT_REQUEST__THANK_YOU_CONTRACTOR', 'CONTACT_REQUEST__THANK_YOU_CONTRACTOR')], db_index=True, max_length=200),
        ),
    ]