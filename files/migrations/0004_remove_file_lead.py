# Generated by Django 3.1.2 on 2021-10-16 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20210904_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='lead',
        ),
    ]
