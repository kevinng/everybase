# Generated by Django 3.0.5 on 2020-10-21 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='types',
        ),
        migrations.DeleteModel(
            name='AddressType',
        ),
    ]