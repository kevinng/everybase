# Generated by Django 3.1.2 on 2021-04-28 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basetruth',
            name='method',
        ),
    ]