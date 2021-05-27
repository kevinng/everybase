# Generated by Django 3.1.2 on 2021-05-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0032_auto_20210527_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagedataboolean',
            name='data_key',
            field=models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING')], db_index=True, default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messagedatafloat',
            name='data_key',
            field=models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING')], db_index=True, default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messagedatastring',
            name='data_key',
            field=models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING')], db_index=True, default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
    ]
