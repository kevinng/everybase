# Generated by Django 3.1.2 on 2021-04-20 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0010_demand_supply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supply',
            options={'verbose_name': 'Supply', 'verbose_name_plural': 'Supplies'},
        ),
    ]