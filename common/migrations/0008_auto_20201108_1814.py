# Generated by Django 3.1.2 on 2020-11-08 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20201108_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importjob',
            name='ended',
        ),
        migrations.RemoveField(
            model_name='importjob',
            name='started',
        ),
    ]
