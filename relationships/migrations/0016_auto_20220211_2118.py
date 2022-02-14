# Generated by Django 3.1.2 on 2022-02-11 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0015_auto_20220206_2224'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='phonenumberhash',
            index_together=None,
        ),
        migrations.RemoveField(
            model_name='phonenumberhash',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='phonenumberhash',
            name='phone_number_type',
        ),
        migrations.RemoveField(
            model_name='phonenumberhash',
            name='user',
        ),
        migrations.DeleteModel(
            name='Connection',
        ),
        migrations.DeleteModel(
            name='PhoneNumberHash',
        ),
    ]
