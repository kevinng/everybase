# Generated by Django 3.1.2 on 2021-06-16 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0058_auto_20210615_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedatavalue',
            name='data_key',
            field=models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('MENU__MENU__OPTION__CHOICE', 'MENU__MENU__OPTION__CHOICE'), ('MENU__MENU__OPTION__FIND_BUYER', 'MENU__MENU__OPTION__FIND_BUYER'), ('MENU__MENU__OPTION__FIND_SELLER', 'MENU__MENU__OPTION__FIND_SELLER'), ('MENU__MENU__OPTION__LEARN_MORE', 'MENU__MENU__OPTION__LEARN_MORE'), ('NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE', 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE'), ('NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG', 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG'), ('NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER', 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER__COUNTRY_STATE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING', 'NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING'), ('NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING', 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING'), ('NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING', 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING'), ('NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING', 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING'), ('NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER', 'NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER'), ('NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE', 'NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE'), ('NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES', 'NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES'), ('NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO', 'NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO'), ('NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING'), ('NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER', 'NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER'), ('NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING', 'NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING'), ('NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING', 'NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING'), ('NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE__PRICE__STRING', 'NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE__PRICE__STRING'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_1__ID', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_1__ID'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_2__ID', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_2__ID'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID'), ('DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__CHOICE', 'DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__CHOICE'), ('DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__YES', 'DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__YES'), ('DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__NO', 'DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__NO'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__CHOICE', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__CHOICE'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__YES', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__YES'), ('DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__NO', 'DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__NO'), ('DISCUSS_W_SELLER__DISCUSS__ASK__QUESTION__STRING', 'DISCUSS_W_SELLER__DISCUSS__ASK__QUESTION__STRING'), ('NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE', 'NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE'), ('NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES', 'NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES'), ('NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO', 'NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO'), ('DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING', 'DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE', 'DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE'), ('DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG', 'DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG'), ('DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER', 'DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER'), ('DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER__COUNTRY_STATE__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER__COUNTRY_STATE__STRING'), ('DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE', 'DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE'), ('DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING__CORRECT__YES', 'DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING__CORRECT__YES'), ('DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING__CORRECT__NO', 'DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING__CORRECT__NO'), ('DISCUSS_W_BUYER__SUPPLY__GET_PACKING__PACKING__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_PACKING__PACKING__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING', 'DISCUSS_W_BUYER__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING'), ('DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER', 'DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER'), ('DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE', 'DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE'), ('DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES', 'DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES'), ('DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO', 'DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO'), ('DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING'), ('DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER', 'DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER'), ('DISCUSS_W_SELLER__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING', 'DISCUSS_W_SELLER__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING'), ('DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING', 'DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING'), ('DISCUSS_W_SELLER__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE__PRICE__STRING', 'DISCUSS_W_SELLER__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE__PRICE__STRING'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__USER_1__ID', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__USER_1__ID'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__USER_2__ID', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__USER_2__ID'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID'), ('DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__CHOICE', 'DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__CHOICE'), ('DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__YES', 'DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__YES'), ('DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__NO', 'DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__NO'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__CHOICE', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__CHOICE'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__YES', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__YES'), ('DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__NO', 'DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__NO'), ('DISCUSS_W_BUYER__DISCUSS__ASK__QUESTION__STRING', 'DISCUSS_W_BUYER__DISCUSS__ASK__QUESTION__STRING'), ('EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE', 'EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE'), ('EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_BUYER', 'EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_BUYER'), ('EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_SELLER', 'EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_SELLER'), ('EXPLAIN_SERIVCE__EXPLAIN_SERVICE__OPTION__LEARN_MORE', 'EXPLAIN_SERIVCE__EXPLAIN_SERVICE__OPTION__LEARN_MORE')], db_index=True, max_length=200),
        ),
    ]
