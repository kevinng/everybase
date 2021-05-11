# Generated by Django 3.1.2 on 2021-05-11 10:41

from django.db import migrations, models
import django.db.models.deletion
import payments.models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0043_companyproducttype'),
        ('payments', '0006_auto_20210511_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlink',
            name='key',
            field=models.CharField(db_index=True, default=payments.models.get_payment_key, max_length=16, unique=True),
        ),
        migrations.AddField(
            model_name='paymentlink',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_links', related_query_name='payment_links', to='relationships.match'),
        ),
        migrations.AddField(
            model_name='paymentlink',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='payment_links', related_query_name='payment_links', to='relationships.user'),
            preserve_default=False,
        ),
    ]
