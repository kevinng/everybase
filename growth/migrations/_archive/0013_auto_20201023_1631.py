# Generated by Django 3.1.2 on 2020-10-23 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0012_lookchemresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='name_1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]