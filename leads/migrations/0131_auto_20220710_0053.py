# Generated by Django 3.1.2 on 2022-07-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0130_auto_20220710_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='need_logistics_logistics_agent',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='need_logistics_other',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
    ]
