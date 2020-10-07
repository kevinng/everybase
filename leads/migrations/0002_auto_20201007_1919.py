# Generated by Django 3.0.5 on 2020-10-07 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplyquote',
            name='able_to_produce_from',
        ),
        migrations.RemoveField(
            model_name='supplyquote',
            name='able_to_produce_reason_md',
        ),
        migrations.RemoveField(
            model_name='supplyquote',
            name='capacity_quantity',
        ),
        migrations.RemoveField(
            model_name='supplyquote',
            name='capacity_seconds',
        ),
        migrations.RemoveField(
            model_name='supplyquote',
            name='unable_to_produce_from',
        ),
        migrations.RemoveField(
            model_name='supplyquote',
            name='unable_to_produce_reason_md',
        ),
        migrations.CreateModel(
            name='ProductCapability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(default=None, null=True)),
                ('start', models.DateTimeField(default=None, null=True)),
                ('end', models.DateTimeField(default=None, null=True)),
                ('capacity_quantity', models.FloatField()),
                ('capacity_seconds', models.FloatField()),
                ('details_md', models.TextField()),
                ('supply_quote', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='production_capabilities', related_query_name='production_capabilities', to='leads.SupplyQuote')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
