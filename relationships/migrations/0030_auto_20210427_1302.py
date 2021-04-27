# Generated by Django 3.1.2 on 2021-04-27 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0029_auto_20210427_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='product_types',
        ),
        migrations.AddField(
            model_name='company',
            name='company_product_types',
            field=models.ManyToManyField(db_index=True, related_name='companies', related_query_name='companies', to='relationships.CompanyProductType'),
        ),
    ]
