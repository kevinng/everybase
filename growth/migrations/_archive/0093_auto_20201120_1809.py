# Generated by Django 3.1.2 on 2020-11-20 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0092_auto_20201120_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemicalclusterofsingaporecompany',
            name='nature_of_business',
            field=models.TextField(blank=True, null=True),
        ),
    ]