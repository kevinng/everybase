# Generated by Django 3.1.2 on 2021-07-23 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0023_auto_20210716_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='display_name',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]