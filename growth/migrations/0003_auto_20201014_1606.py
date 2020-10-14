# Generated by Django 3.0.5 on 2020-10-14 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0020_auto_20201014_1454'),
        ('growth', '0002_auto_20201014_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Address'),
        ),
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Company'),
        ),
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Email'),
        ),
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.Link'),
        ),
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='phone_numbers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemical_cluster_of_singapore_results', related_query_name='chemical_cluster_of_singapore_results', to='relationships.PhoneNumber'),
        ),
        migrations.AlterField(
            model_name='gmasscampaign',
            name='campaign_id',
            field=models.CharField(default=-1, max_length=100),
            preserve_default=False,
        ),
    ]
