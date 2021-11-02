# Generated by Django 3.1.2 on 2021-10-30 06:06

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_contactrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length='7', prefix='', primary_key=True, serialize=False),
        ),
    ]