# Generated by Django 3.1.2 on 2021-05-18 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0020_auto_20210518_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twiliooutboundmessage',
            name='message_template',
        ),
        migrations.AddField(
            model_name='twiliooutboundmessage',
            name='message_type',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='MessageTemplate',
        ),
    ]
