# Generated by Django 3.1.2 on 2021-06-19 13:01

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0018_auto_20210618_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthash',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length='7', prefix='', primary_key=True, serialize=False),
        ),
    ]