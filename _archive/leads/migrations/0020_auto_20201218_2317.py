# Generated by Django 3.1.2 on 2020-12-18 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0019_auto_20201218_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='public_details_url',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='public_details_url',
        ),
    ]