# Generated by Django 3.1.2 on 2021-10-16 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0025_auto_20210730_1216'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='paymenthash',
            unique_together=set(),
        ),
        # migrations.RemoveField(
        #     model_name='paymenthash',
        #     name='match',
        # ),
    ]
