# Generated by Django 3.1.2 on 2021-04-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20210428_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetemplate',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='messagetemplate',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='twilioinboundmessage',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='twiliooutboundmessage',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
