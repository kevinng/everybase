# Generated by Django 3.0.5 on 2020-10-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20201021_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='cc_tld',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='CC TLD'),
        ),
    ]
