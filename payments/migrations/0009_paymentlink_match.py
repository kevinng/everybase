# Generated by Django 3.1.2 on 2021-05-12 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_auto_20210512_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlink',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_links', related_query_name='payment_links', to='relationships.match'),
        ),
    ]
