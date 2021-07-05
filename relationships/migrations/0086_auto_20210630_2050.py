# Generated by Django 3.1.2 on 2021-06-30 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0107_auto_20210630_2050'),
        ('relationships', '0085_user_current_match_to_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='buyer_confirmed_still_interested',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='buyer_still_interested',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='buyer_still_interested_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='matches_w_this_buyer_still_interested_value', related_query_name='matches_w_this_buyer_still_interested_value', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='match',
            name='seller_confirmed_still_interested',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='seller_still_interested',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='seller_still_interested_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='matches_w_this_seller_still_interested_value', related_query_name='matches_w_this_seller_still_interested_value', to='chat.messagedatavalue'),
        ),
    ]
