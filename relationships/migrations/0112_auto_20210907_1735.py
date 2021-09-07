# Generated by Django 3.1.2 on 2021-09-07 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0111_leadtext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='can_source',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='interested_product_type',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='is_direct',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='not_interested_details',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='not_interested_details_reason',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='responded_can_source',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='responded_interested_product_type',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='responded_is_direct',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='responded_not_interested_details',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='responded_not_interested_details_reason',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommend_details_choice',
            field=models.CharField(blank=True, choices=[('RECOMMEND__DETAILS__DIRECT', 'RECOMMEND__DETAILS__DIRECT'), ('RECOMMEND__DETAILS__CAN_FIND', 'RECOMMEND__DETAILS__CAN_FIND'), ('RECOMMEND__DETAILS__NOT_NOW', 'RECOMMEND__DETAILS__NOT_NOW'), ('RECOMMEND__DETAILS__NOT_INTERESTED', 'RECOMMEND__DETAILS__NOT_INTERESTED')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommend_details_not_interested_responded',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommend_details_not_interested_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommend_details_responded',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommend_product_type_choice',
            field=models.CharField(blank=True, choices=[('RECOMMEND__PRODUCT_TYPE_YES', 'RECOMMEND__PRODUCT_TYPE_YES'), ('RECOMMEND__PRODUCT_TYPE__NOT_NOW', 'RECOMMEND__PRODUCT_TYPE__NOT_NOW'), ('RECOMMEND__PRODUCT_TYPE__NO', 'RECOMMEND__PRODUCT_TYPE__NO')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommend_product_type_responded',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
