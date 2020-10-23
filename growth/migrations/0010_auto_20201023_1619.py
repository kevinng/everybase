# Generated by Django 3.1.2 on 2020-10-23 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_country_cc_tld'),
        ('growth', '0009_chemicalbookresultcountrytype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalBookResultCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('details_md', models.TextField(verbose_name='Details in Markdown')),
                ('chemical_book_result', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemicalbookresult_country_relationships', related_query_name='chemicalbookresult_country_relationships', to='growth.chemicalbookresult')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemicalbookresult_country_relationships', related_query_name='chemicalbookresult_country_relationships', to='common.country')),
                ('rtype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chemicalbookresult_country_relationships', related_query_name='chemicalbookresult_country_relationships', to='growth.chemicalbookresultcountrytype', verbose_name='ChemicalBookResult-Country Type')),
            ],
            options={
                'verbose_name': 'ChemicalBookResult-Country Relationship',
                'verbose_name_plural': 'ChemicalBookResult-Country Relationships',
            },
        ),
        migrations.AddField(
            model_name='chemicalbookresult',
            name='country',
            field=models.ManyToManyField(related_name='chemical_book_results', related_query_name='chemical_book_results', through='growth.ChemicalBookResultCountry', to='common.Country'),
        ),
    ]
