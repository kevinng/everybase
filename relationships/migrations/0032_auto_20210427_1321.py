# Generated by Django 3.1.2 on 2021-04-27 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0031_auto_20210427_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyproduct',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_products', related_query_name='company_products', to='relationships.company'),
        ),
        migrations.AlterField(
            model_name='companyproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_products', related_query_name='company_products', to='relationships.product'),
        ),
    ]
