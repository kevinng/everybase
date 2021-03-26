# Generated by Django 3.1.2 on 2021-03-26 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_auto_20201217_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='details_md',
        ),
        migrations.RemoveField(
            model_name='language',
            name='details_md',
        ),
        migrations.RemoveField(
            model_name='state',
            name='details_md',
        ),
        migrations.AddField(
            model_name='country',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='language',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
