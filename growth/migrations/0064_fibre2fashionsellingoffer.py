# Generated by Django 3.1.2 on 2020-11-10 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20201109_1500'),
        ('relationships', '0015_auto_20201110_1148'),
        ('growth', '0063_auto_20201110_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fibre2FashionSellingOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('harvested', models.DateTimeField(db_index=True)),
                ('source_link', models.CharField(db_index=True, max_length=300)),
                ('category', models.CharField(db_index=True, max_length=100)),
                ('sub_category', models.CharField(db_index=True, max_length=100)),
                ('title', models.CharField(max_length=300)),
                ('reference_no', models.CharField(db_index=True, max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('email_str', models.CharField(db_index=True, max_length=100)),
                ('company_name', models.CharField(db_index=True, max_length=100)),
                ('company_address', models.CharField(db_index=True, max_length=300)),
                ('product_info_html', models.TextField()),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fibre2fashion_selling_offer_emails', related_query_name='fibre2fashion_selling_offer_emails', to='relationships.email')),
                ('import_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fibre2fashion_selling_offers', related_query_name='fibre2fashion_selling_offers', to='common.importjob')),
                ('invalid_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fibre2fashion_selling_offer_invalid_emails', related_query_name='fibre2fashion_selling_offer_invalid_emails', to='relationships.invalidemail')),
            ],
            options={
                'verbose_name': 'Fibre2Fashion selling offer',
                'verbose_name_plural': 'Fibre2Fashion selling offers',
            },
        ),
    ]