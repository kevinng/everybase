# Generated by Django 3.1.2 on 2021-06-17 09:55

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        # ('relationships', '0075_auto_20210617_1745'),
        ('payments', '0011_auto_20210617_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHash',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('started', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('succeeded', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('failed', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('session_id', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('unit_amount', models.FloatField(blank=True, db_index=True, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_hashes', related_query_name='payment_hashes', to='payments.currency')),
                ('match', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_links', related_query_name='payment_links', to='relationships.match')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_links', related_query_name='payment_links', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='paymentevent',
            name='payment_link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_events', related_query_name='payment_events', to='payments.paymenthash'),
        ),
        migrations.DeleteModel(
            name='PaymentLink',
        ),
    ]
