# Generated by Django 3.1.2 on 2021-09-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0114_recommendation_recommend_product_type_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='recommend_details_choice',
            field=models.CharField(blank=True, choices=[('RECOMMEND__DETAILS__IMMEDIATE', 'RECOMMEND__DETAILS__IMMEDIATE'), ('RECOMMEND__DETAILS__NEED_TIME', 'RECOMMEND__DETAILS__NEED_TIME'), ('RECOMMEND__DETAILS__NOT_INTERESTED', 'RECOMMEND__DETAILS__NOT_INTERESTED')], max_length=200, null=True),
        ),
    ]
