# Generated by Django 3.1.2 on 2021-06-20 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0060_auto_20210617_1331'),
        ('relationships', '0078_auto_20210619_2101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='country_state_captured',
        ),
        migrations.RemoveField(
            model_name='demand',
            name='packing_captured',
        ),
        migrations.RemoveField(
            model_name='demand',
            name='price_captured',
        ),
        migrations.RemoveField(
            model_name='demand',
            name='product_type_captured',
        ),
        migrations.RemoveField(
            model_name='demand',
            name='quantity_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='accept_lc_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='availability_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='country_state_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='deposit_percentage_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='packing_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='pre_order_timeframe_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='price_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='product_type_captured',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='quantity_captured',
        ),
        migrations.AddField(
            model_name='demand',
            name='country_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_country_values', related_query_name='demand_country_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='country_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='currency_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_currency_values', related_query_name='demand_currency_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='currency_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='packing_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_packing_values', related_query_name='demand_packing_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='packing_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='price_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_price_values', related_query_name='demand_price_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='price_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='product_type_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_product_type_values', related_query_name='demand_product_type_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='product_type_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='quantity_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_quantity_values', related_query_name='demand_quantity_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='quantity_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='state_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_state_values', related_query_name='demand_state_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='demand',
            name='state_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='accept_lc_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_accept_lc_values', related_query_name='supply_accept_lc_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='accept_lc_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='availability_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_availability_values', related_query_name='supply_availability_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='availability_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='country_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_country_values', related_query_name='supply_country_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='country_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='currency_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_currency_values', related_query_name='supply_currency_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='currency_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='deposit_percentage_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_deposit_percentage_values', related_query_name='supply_deposit_percentage_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='deposit_percentage_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='packing_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_packing_values', related_query_name='supply_packing_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='packing_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='pre_order_timeframe_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_pre_order_timeframe_values', related_query_name='supply_pre_order_timeframe_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='pre_order_timeframe_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='price_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_price_values', related_query_name='supply_price_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='price_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='product_type_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_product_type_values', related_query_name='supply_product_type_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='product_type_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='quantity_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_quantity_values', related_query_name='supply_quantity_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='quantity_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='state_data_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_state_values', related_query_name='supply_state_values', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='supply',
            name='state_method',
            field=models.CharField(blank=True, choices=[], db_index=True, max_length=200, null=True),
        ),
    ]
