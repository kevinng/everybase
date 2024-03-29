# Generated by Django 3.1.2 on 2020-11-06 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_country_cc_tld'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='cc_tld',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='CC TLD'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='country',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='state',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]
