# Generated by Django 3.1.2 on 2020-11-14 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20201109_1500'),
        ('growth', '0078_auto_20201114_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='OKChemBuyingRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('harvested', models.DateTimeField(db_index=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('request', models.TextField(blank=True, db_index=True, null=True)),
                ('email', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('import_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ok_chem_buying_requests', related_query_name='ok_chem_buying_requests', to='common.importjob')),
            ],
            options={
                'verbose_name': 'OKChem buying request',
                'verbose_name_plural': 'OKChem buying requests',
            },
        ),
        migrations.DeleteModel(
            name='OKChemResult',
        ),
    ]
