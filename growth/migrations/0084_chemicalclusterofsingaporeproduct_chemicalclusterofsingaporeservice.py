# Generated by Django 3.1.2 on 2020-11-16 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20201109_1500'),
        ('growth', '0083_chemicalclusterofsingaporecompany'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalClusterOfSingaporeService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('harvested', models.DateTimeField(db_index=True)),
                ('source_url', models.CharField(db_index=True, max_length=300)),
                ('company_name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('service', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('import_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_services', related_query_name='chemical_cluster_of_singapore_services', to='common.importjob')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChemicalClusterOfSingaporeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('harvested', models.DateTimeField(db_index=True)),
                ('source_url', models.CharField(db_index=True, max_length=300)),
                ('company_name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('product', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('import_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_products', related_query_name='chemical_cluster_of_singapore_products', to='common.importjob')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
