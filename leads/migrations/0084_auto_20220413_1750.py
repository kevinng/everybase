# Generated by Django 3.1.2 on 2022-04-13 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0083_auto_20220413_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leadquerylog',
            old_name='goods_string',
            new_name='goods_services',
        ),
    ]
