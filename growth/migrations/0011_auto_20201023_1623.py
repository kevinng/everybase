# Generated by Django 3.1.2 on 2020-10-23 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0010_auto_20201023_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chemicalbookresult',
            old_name='country',
            new_name='countries',
        ),
        migrations.RenameField(
            model_name='chemicalbookresult',
            old_name='email',
            new_name='emails',
        ),
    ]
