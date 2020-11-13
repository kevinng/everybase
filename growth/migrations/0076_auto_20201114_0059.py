# Generated by Django 3.1.2 on 2020-11-13 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0015_auto_20201110_1148'),
        ('common', '0010_auto_20201109_1500'),
        ('growth', '0075_auto_20201113_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorldOfChemicalsSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('harvested', models.DateTimeField(db_index=True)),
                ('source_url', models.CharField(blank=True, db_index=True, max_length=300, null=True)),
                ('coy_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_about_html', models.TextField(blank=True, null=True)),
                ('coy_pri_contact', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_addr_1', models.CharField(blank=True, max_length=500, null=True)),
                ('coy_addr_2', models.CharField(blank=True, max_length=500, null=True)),
                ('coy_city', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_state', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_country', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_postal', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_phone', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_phone_2', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_email', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_owner_email', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_alt_email', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_alt_email_2', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_alt_email_3', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('coy_website', models.CharField(blank=True, db_index=True, max_length=300, null=True)),
                ('alt_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_alt_emails', related_query_name='world_of_chemicals_supplier_alt_emails', to='relationships.email')),
                ('alt_email_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_alt_email_2s', related_query_name='world_of_chemicals_supplier_alt_email_2s', to='relationships.email')),
                ('alt_email_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_alt_email_3s', related_query_name='world_of_chemicals_supplier_alt_email_3s', to='relationships.email')),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_emails', related_query_name='world_of_chemicals_supplier_emails', to='relationships.email')),
                ('import_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_results', related_query_name='world_of_chemicals_supplier_results', to='common.importjob')),
                ('invalid_alt_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_invalid_alt_emails', related_query_name='world_of_chemicals_supplier_invalid_alt_emails', to='relationships.invalidemail')),
                ('invalid_alt_email_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_invalid_alt_email_2s', related_query_name='world_of_chemicals_supplier_invalid_alt_email_2s', to='relationships.invalidemail')),
                ('invalid_alt_email_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_invalid_alt_email_3s', related_query_name='world_of_chemicals_supplier_invalid_alt_email_3s', to='relationships.invalidemail')),
                ('invalid_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_invalid_emails', related_query_name='world_of_chemicals_supplier_invalid_emails', to='relationships.invalidemail')),
                ('invalid_owner_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_invalid_owner_emails', related_query_name='world_of_chemicals_supplier_invalid_owner_emails', to='relationships.invalidemail')),
                ('owner_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='world_of_chemicals_supplier_owner_emails', related_query_name='world_of_chemicals_supplier_owner_emails', to='relationships.email')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultaddress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultaddress',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultaddress',
            name='world_of_chemicals_result',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultcompany',
            name='company',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultcompany',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultcompany',
            name='world_of_chemicals_result',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultemail',
            name='email',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultemail',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultemail',
            name='world_of_chemicals_result',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultlink',
            name='link',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultlink',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultlink',
            name='world_of_chemicals_result',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultphonenumber',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultphonenumber',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='worldofchemicalsresultphonenumber',
            name='world_of_chemicals_result',
        ),
        migrations.AddField(
            model_name='okchemresult',
            name='import_job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ok_chem_results', related_query_name='ok_chem_results', to='common.importjob'),
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResult',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultAddress',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultAddressType',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultCompany',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultCompanyType',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultEmail',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultEmailType',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultLink',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultLinkType',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultPhoneNumber',
        ),
        migrations.DeleteModel(
            name='WorldOfChemicalsResultPhoneNumberType',
        ),
    ]
