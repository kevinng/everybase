# Generated by Django 3.0.2 on 2020-01-23 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='batch',
            unique_together={('material', 'code')},
        ),
    ]
