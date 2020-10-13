# Generated by Django 3.0.5 on 2020-10-13 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0011_auto_20201013_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyaddress',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_address_relationships', related_query_name='company_address_relationships', to='relationships.Address'),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_address_relationships', related_query_name='company_address_relationships', to='relationships.Company'),
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='rtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_address_relationships', related_query_name='company_address_relationships', to='relationships.CompanyAddressType', verbose_name='Company-address relationship type'),
        ),
    ]
