# Generated by Django 3.1.2 on 2021-06-18 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_paymenthash_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlinkaccess',
            name='outcome',
            field=models.CharField(blank=True, choices=[('successful', 'Successful'), ('failed', 'Failed')], db_index=True, max_length=200, null=True),
        ),
    ]