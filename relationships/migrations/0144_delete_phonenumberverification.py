# Generated by Django 3.1.2 on 2021-10-29 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0143_friendrequest'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhoneNumberVerification',
        ),
    ]