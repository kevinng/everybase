# Generated by Django 3.1.2 on 2020-10-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0002_auto_20201022_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalBookResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('source_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='Source URL')),
                ('coy_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company name')),
                ('coy_internal_href', models.CharField(blank=True, max_length=100, null=True, verbose_name='Details page URL')),
                ('coy_tel', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company telephone')),
                ('coy_email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company email')),
                ('coy_href', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company website')),
                ('coy_nat', models.CharField(blank=True, max_length=100, null=True, verbose_name='Country')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
