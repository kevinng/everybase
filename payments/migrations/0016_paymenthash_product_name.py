# Generated by Django 3.1.2 on 2021-06-18 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0015_paymenthash_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthash',
            name='product_name',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]