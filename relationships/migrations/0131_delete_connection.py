# Generated by Django 3.1.2 on 2021-10-16 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0130_delete_supply'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Connection',
        ),
    ]