# Generated by Django 3.1.2 on 2021-09-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0139_auto_20210914_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedatavalue',
            name='data_key',
            field=models.CharField(choices=[('NO_DATA', 'NO_DATA'), ('STRAY_INPUT', 'STRAY_INPUT'), ('INVALID_CHOICE', 'INVALID_CHOICE'), ('MENU__FIND_BUYERS', 'MENU__FIND_BUYERS'), ('MENU__FIND_SELLERS', 'MENU__FIND_SELLERS'), ('MENU__TALK_TO_AN_EVERYBASE_AGENT', 'MENU__TALK_TO_AN_EVERYBASE_AGENT'), ('MENU__REGISTER_ME', 'MENU__REGISTER_ME'), ('RECOMMEND__PRODUCT_TYPE', 'RECOMMEND__PRODUCT_TYPE'), ('RECOMMEND__PRODUCT_TYPE_YES', 'RECOMMEND__PRODUCT_TYPE_YES'), ('RECOMMEND__PRODUCT_TYPE__NOT_NOW', 'RECOMMEND__PRODUCT_TYPE__NOT_NOW'), ('RECOMMEND__PRODUCT_TYPE__NO', 'RECOMMEND__PRODUCT_TYPE__NO'), ('RECOMMEND__DETAILS', 'RECOMMEND__DETAILS'), ('RECOMMEND__DETAILS__IMMEDIATE', 'RECOMMEND__DETAILS__IMMEDIATE'), ('RECOMMEND__DETAILS__NEED_TIME', 'RECOMMEND__DETAILS__NEED_TIME'), ('RECOMMEND__DETAILS__NOT_INTERESTED', 'RECOMMEND__DETAILS__NOT_INTERESTED')], db_index=True, max_length=200),
        ),
    ]
