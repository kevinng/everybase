# Generated by Django 3.1.2 on 2021-04-19 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0004_accessedurl_useripdevice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('display_name', models.CharField(db_index=True, max_length=200)),
                ('notes', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='accessedurl',
            options={'verbose_name': 'Accessed URL', 'verbose_name_plural': 'Accessed URLs'},
        ),
        migrations.AlterModelOptions(
            name='useripdevice',
            options={'verbose_name': 'User IP-Device', 'verbose_name_plural': 'User IP-Devices'},
        ),
        migrations.AlterField(
            model_name='accessedurl',
            name='url',
            field=models.URLField(db_index=True, unique=True, verbose_name='URL'),
        ),
        migrations.CreateModel(
            name='CompanyProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('popularity', models.FloatField(db_index=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='relationships.company')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='relationships.producttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='company',
            name='product_types',
            field=models.ManyToManyField(related_name='companies', related_query_name='companies', through='relationships.CompanyProductType', to='relationships.ProductType'),
        ),
    ]