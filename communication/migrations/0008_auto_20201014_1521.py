# Generated by Django 3.0.5 on 2020-10-14 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0007_auto_20201014_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='scheduled',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
