# Generated by Django 3.0.5 on 2020-10-14 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relationships', '0019_auto_20201013_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details_md', models.TextField(blank=True, null=True, verbose_name='Details in Markdown')),
                ('programmatic_key', models.CharField(blank=True, max_length=100, null=True)),
                ('programmatic_details_md', models.TextField(blank=True, null=True, verbose_name='Programmatic details in Markdown')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GmassCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('campaign_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sent', models.DateTimeField(blank=True, default=None, null=True)),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('spreadsheet', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ZeroBounceResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.CharField(max_length=100)),
                ('sub_status', models.CharField(max_length=100)),
                ('account', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('free_email', models.CharField(max_length=100)),
                ('mx_found', models.CharField(max_length=100)),
                ('mx_record', models.CharField(max_length=100)),
                ('smtp_provider', models.CharField(max_length=100)),
                ('did_you_mean', models.CharField(max_length=100)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='zero_bounce_results', related_query_name='zero_bounce_results', to='relationships.Email')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourcedEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('sourced', models.DateTimeField(blank=True, default=None, null=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sourced_emails', related_query_name='sourced_emails', to='relationships.Email')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sourced_emails', related_query_name='sourced_emails', to='growth.DataSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GmassCampaignResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('name_1', models.CharField(blank=True, max_length=100, null=True)),
                ('opens', models.CharField(blank=True, max_length=100, null=True)),
                ('clicks', models.CharField(blank=True, max_length=100, null=True)),
                ('replied', models.CharField(blank=True, max_length=100, null=True)),
                ('unsubscribed', models.CharField(blank=True, max_length=100, null=True)),
                ('bounced', models.CharField(blank=True, max_length=100, null=True)),
                ('blocked', models.CharField(blank=True, max_length=100, null=True)),
                ('over_gmail_limit', models.CharField(blank=True, max_length=100, null=True)),
                ('bounce_reason', models.TextField(blank=True, null=True)),
                ('gmail_response', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gmass_campaign_results', related_query_name='gmass_campaign_results', to='relationships.Email')),
                ('gmass_compaign', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='results', related_query_name='results', to='growth.GmassCampaign')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fibre2FashionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('sourced', models.DateTimeField(blank=True, default=None, null=True)),
                ('source_link', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('sub_category', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('email_domain', models.CharField(max_length=100)),
                ('lead_type', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('emails', models.ManyToManyField(related_name='fibre2fashion_results', related_query_name='fibre2fashion_results', to='relationships.Email')),
                ('links', models.ManyToManyField(related_name='fibre2fashion_results', related_query_name='fibre2fashion_results', to='relationships.Link')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='datasource',
            name='emails',
            field=models.ManyToManyField(related_name='data_sources', related_query_name='data_sources', through='growth.SourcedEmail', to='relationships.Email'),
        ),
        migrations.CreateModel(
            name='ChemicalClusterOfSingaporeResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('sourced', models.DateTimeField(blank=True, default=None, null=True)),
                ('company_name', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=100)),
                ('fax', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
                ('source_link', models.CharField(max_length=100)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Address')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Company')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Email')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Link')),
                ('phone_numbers', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.PhoneNumber')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
