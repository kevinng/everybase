# Generated by Django 3.1.2 on 2021-05-14 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_twilioinboundmessage_sms_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twilioinboundmessage',
            old_name='num_segment',
            new_name='num_segments',
        ),
    ]