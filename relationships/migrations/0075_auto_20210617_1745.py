# Generated by Django 3.1.2 on 2021-06-17 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0074_auto_20210616_0002'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PhoneNumberURLAccess',
            new_name='PhoneNumberLinkAccess',
        ),
    ]
