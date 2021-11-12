# Generated by Django 3.1.2 on 2021-11-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_delete_matchkeyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='country_code',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='dial_code',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='flag_url',
            field=models.URLField(blank=True, db_index=True, null=True),
        ),
    ]
