# Generated by Django 3.1.2 on 2022-01-26 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('leads', '0008_lead_hide_commission_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='avg_comm_pct',
            field=models.FloatField(db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='avg_deal_size',
            field=models.FloatField(db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='buy_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lead_with_this_buy_country', related_query_name='lead_with_this_buy_country', to='common.country'),
        ),
        migrations.AddField(
            model_name='lead',
            name='sell_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lead_with_this_sell_country', related_query_name='lead_with_this_sell_country', to='common.country'),
        ),
    ]