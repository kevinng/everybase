# Generated by Django 3.1.2 on 2020-11-04 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0040_auto_20201025_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='category',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='description',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='email',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='email_domain',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='lead_type',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='source_link',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='sub_category',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='blocked',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='bounced',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='clicks',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='email_address',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='gmail_response',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='name_1',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='opens',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='over_gmail_limit',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='replied',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='unsubscribed',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]
