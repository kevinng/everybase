# Generated by Django 3.1.2 on 2020-11-21 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0095_auto_20201121_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmasscampaign',
            name='spreadsheet',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaign',
            name='subject',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
