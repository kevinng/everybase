# Generated by Django 3.1.2 on 2021-08-24 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0018_auto_20210824_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='cc_users',
        ),
    ]
