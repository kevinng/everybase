# Generated by Django 3.1.2 on 2021-05-27 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0065_auto_20210527_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='country',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]