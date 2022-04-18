# Generated by Django 3.1.2 on 2022-02-16 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('leads', '0034_auto_20220216_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='buy_country',
            # field=models.ForeignKey(default=696, on_delete=django.db.models.deletion.PROTECT, related_name='lead_with_this_buy_country', related_query_name='lead_with_this_buy_country', to='common.country'),
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lead_with_this_buy_country', related_query_name='lead_with_this_buy_country', to='common.country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lead',
            name='sell_country',
            # field=models.ForeignKey(default=696, on_delete=django.db.models.deletion.PROTECT, related_name='lead_with_this_sell_country', related_query_name='lead_with_this_sell_country', to='common.country'),
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lead_with_this_sell_country', related_query_name='lead_with_this_sell_country', to='common.country'),
            preserve_default=False,
        ),
    ]
