# Generated by Django 3.1.2 on 2022-02-07 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0020_leadquery_sort_by'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContactRequest',
        ),
    ]
