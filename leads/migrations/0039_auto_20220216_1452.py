# Generated by Django 3.1.2 on 2022-02-16 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0038_auto_20220216_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='commissions',
            new_name='commission',
        ),
    ]