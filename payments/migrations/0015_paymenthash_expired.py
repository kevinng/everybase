# Generated by Django 3.1.2 on 2021-06-18 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_paymentlinkaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthash',
            name='expired',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
