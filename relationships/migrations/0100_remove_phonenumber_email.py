# Generated by Django 3.1.2 on 2021-08-11 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0099_auto_20210811_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumber',
            name='email',
        ),
    ]
