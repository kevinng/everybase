# Generated by Django 3.1.2 on 2022-10-05 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0093_statusfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statusfile',
            old_name='csrf',
            new_name='form_uuid',
        ),
    ]
