# Generated by Django 3.1.2 on 2021-05-12 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0046_delete_locationproductspecificationtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='demand_quote',
        ),
        migrations.RemoveField(
            model_name='match',
            name='supply_quote',
        ),
    ]
