# Generated by Django 3.1.2 on 2021-05-11 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_paymentevent_paymenteventtype_stripesession'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StripeSession',
            new_name='PaymentLink',
        ),
    ]
