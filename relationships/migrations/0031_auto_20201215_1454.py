# Generated by Django 3.1.2 on 2020-12-15 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0030_auto_20201215_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='country_code',
            field=models.CharField(db_index=True, default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='national_number',
            field=models.CharField(db_index=True, default=None, max_length=100),
        ),
    ]