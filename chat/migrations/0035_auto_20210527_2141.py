# Generated by Django 3.1.2 on 2021-05-27 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0034_auto_20210527_2125'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='messagedatavalue',
            unique_together={('dataset', 'data_key')},
        ),
    ]