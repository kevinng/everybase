# Generated by Django 3.1.2 on 2022-02-18 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_auto_20220219_0434'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set(),
        ),
    ]
