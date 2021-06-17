# Generated by Django 3.1.2 on 2021-06-17 05:31

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_auto_20210516_0155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentlink',
            name='key',
        ),
        migrations.AlterField(
            model_name='paymentlink',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False),
        ),
    ]
