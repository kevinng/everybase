# Generated by Django 3.1.2 on 2020-10-25 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0034_auto_20201025_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookchemresult',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]