# Generated by Django 3.1.2 on 2021-04-20 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0009_productspecificationtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supply_leads', related_query_name='supply_leads', to='relationships.company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supply_leads', related_query_name='supply_leads', to='relationships.product')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supply_leads', related_query_name='supply_leads', to='relationships.producttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supply_leads', related_query_name='supply_leads', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_leads', related_query_name='demand_leads', to='relationships.company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_leads', related_query_name='demand_leads', to='relationships.product')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_leads', related_query_name='demand_leads', to='relationships.producttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_leads', related_query_name='demand_leads', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]