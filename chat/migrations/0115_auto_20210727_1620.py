# Generated by Django 3.1.2 on 2021-07-27 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0114_auto_20210715_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twiliooutboundmessage',
            name='date_created',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='twiliooutboundmessage',
            name='date_sent',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
