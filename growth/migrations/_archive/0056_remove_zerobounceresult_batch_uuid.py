# Generated by Django 3.1.2 on 2020-11-07 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0055_auto_20201107_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zerobounceresult',
            name='batch_uuid',
        ),
    ]