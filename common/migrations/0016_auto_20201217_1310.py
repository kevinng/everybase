# Generated by Django 3.1.2 on 2020-12-17 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_state_china_province_name_cn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='china_province_name_cn',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='China province name in Chinese'),
        ),
    ]