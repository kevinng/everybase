# Generated by Django 3.0.4 on 2020-04-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('source_url', models.CharField(db_index=True, max_length=200)),
                ('coy_name', models.CharField(db_index=True, max_length=1024)),
                ('coy_internal_href', models.CharField(db_index=True, max_length=1024)),
                ('coy_tel', models.CharField(db_index=True, max_length=1024)),
                ('coy_email', models.CharField(db_index=True, max_length=1024)),
                ('coy_href', models.CharField(db_index=True, max_length=1024)),
                ('coy_nat', models.CharField(db_index=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Fibre2FashionLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('url', models.CharField(db_index=True, max_length=1024)),
                ('cat', models.CharField(db_index=True, max_length=1024)),
                ('subcat', models.CharField(db_index=True, max_length=1024)),
                ('title', models.CharField(db_index=True, max_length=1024)),
                ('ref_no', models.CharField(db_index=True, max_length=1024)),
                ('biz_lead', models.CharField(db_index=True, max_length=1024)),
                ('coy_name', models.CharField(db_index=True, max_length=1024)),
                ('coy_addr', models.CharField(db_index=True, max_length=1024)),
                ('coy_desc', models.TextField()),
                ('coy_email', models.CharField(db_index=True, max_length=1024)),
                ('prod_info_html', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LookChemSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('coy_name', models.CharField(db_index=True, max_length=1024)),
                ('contact_person', models.CharField(db_index=True, max_length=1024)),
                ('street_person', models.CharField(db_index=True, max_length=1024)),
                ('city', models.CharField(db_index=True, max_length=1024)),
                ('province_state', models.CharField(db_index=True, max_length=1024)),
                ('country_region', models.CharField(db_index=True, max_length=1024)),
                ('zip_code', models.CharField(db_index=True, max_length=1024)),
                ('business_type', models.CharField(db_index=True, max_length=1024)),
                ('tel', models.CharField(db_index=True, max_length=1024)),
                ('mobile', models.CharField(db_index=True, max_length=1024)),
                ('email', models.CharField(db_index=True, max_length=1024)),
                ('website', models.CharField(db_index=True, max_length=1024)),
                ('qq', models.CharField(db_index=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='WorldOfChemicalsSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('coy_name', models.CharField(db_index=True, max_length=1024)),
                ('coy_about_html', models.TextField(blank=True)),
                ('coy_primary_contact', models.CharField(db_index=True, max_length=1024)),
                ('coy_addr_1', models.CharField(max_length=1024)),
                ('coy_addr_2', models.CharField(max_length=1024)),
                ('coy_city', models.CharField(db_index=True, max_length=1024)),
                ('coy_state', models.CharField(db_index=True, max_length=1024)),
                ('coy_country', models.CharField(db_index=True, max_length=1024)),
                ('coy_postal', models.CharField(db_index=True, max_length=1024)),
                ('coy_phone', models.CharField(db_index=True, max_length=1024)),
                ('coy_phone_2', models.CharField(db_index=True, max_length=1024)),
                ('coy_email', models.CharField(db_index=True, max_length=1024)),
                ('coy_owner_email', models.CharField(db_index=True, max_length=1024)),
                ('coy_alt_email', models.CharField(db_index=True, max_length=1024)),
                ('coy_alt_email_2', models.CharField(db_index=True, max_length=1024)),
                ('coy_alt_email_3', models.CharField(db_index=True, max_length=1024)),
                ('coy_website', models.CharField(db_index=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='ZeroBounceResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('email_address', models.CharField(db_index=True, max_length=1024)),
                ('zb_status', models.CharField(db_index=True, max_length=1024)),
                ('zb_sub_status', models.CharField(db_index=True, max_length=1024)),
                ('zb_account', models.CharField(db_index=True, max_length=1024)),
                ('zb_domain', models.CharField(db_index=True, max_length=1024)),
                ('zb_first_name', models.CharField(max_length=1024)),
                ('zb_last_name', models.CharField(max_length=1024)),
                ('zb_gender', models.CharField(db_index=True, max_length=1024)),
                ('zb_free_email', models.BooleanField(db_index=True)),
                ('zb_mx_found', models.BooleanField(db_index=True)),
                ('zb_mx_record', models.CharField(db_index=True, max_length=1024)),
                ('zb_smtp_provider', models.CharField(db_index=True, max_length=1024)),
                ('zb_did_you_mean', models.CharField(db_index=True, max_length=1024)),
            ],
        ),
    ]
