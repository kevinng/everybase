# Generated by Django 3.1.2 on 2022-02-16 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0039_auto_20220216_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='other_comm_details',
            new_name='other_agent_details',
        ),
    ]