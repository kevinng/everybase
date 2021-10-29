# Generated by Django 3.1.2 on 2021-04-25 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # ('relationships', '0028_auto_20210422_1752'),
        ('payments', '0002_auto_20210421_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StripeSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('started', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('succeeded', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('failed', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('session_id', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('unit_amount', models.FloatField(blank=True, db_index=True, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stripe_sessions', related_query_name='stripe_sessions', to='payments.currency')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('amount', models.FloatField(db_index=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_events', related_query_name='payment_events', to='payments.currency')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_events', related_query_name='payment_events', to='payments.paymenteventtype')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_events', related_query_name='payment_events', to='relationships.match')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_events', related_query_name='payment_events', to='payments.stripesession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_events', related_query_name='payment_events', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
