# Generated by Django 3.1.2 on 2021-11-12 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20211112_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
