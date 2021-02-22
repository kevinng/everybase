# Generated by Django 3.1.2 on 2021-01-14 11:19

from django.db import migrations, models
import relationships.models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0050_auto_20210114_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='country_code',
            field=models.CharField(db_index=True, default=None, max_length=50, validators=[relationships.models.validate_phone_number_country_code]),
        ),
    ]