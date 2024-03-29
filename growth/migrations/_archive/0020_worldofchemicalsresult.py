# Generated by Django 3.1.2 on 2020-10-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0019_auto_20201023_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorldOfChemicalsResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('source_url', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_id', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_name', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_about_html', models.TextField(blank=True, null=True)),
                ('coy_pri_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_addr_1', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_addr_2', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_city', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_state', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_country', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_postal', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_phone_2', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_email', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_owner_email', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_alt_email', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_alt_email_2', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_alt_email_3', models.CharField(blank=True, max_length=100, null=True)),
                ('coy_website', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
