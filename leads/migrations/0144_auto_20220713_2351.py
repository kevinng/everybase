# Generated by Django 3.1.2 on 2022-07-13 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0143_auto_20220713_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='session_key',
            new_name='cookie_uuid',
        ),
    ]