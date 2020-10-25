# Generated by Django 3.1.2 on 2020-10-25 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0037_lookchemresult_email_as_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lookchemresult',
            name='email_as_email',
        ),
        migrations.RemoveField(
            model_name='lookchemresult',
            name='website_as_url',
        ),
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='source_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='chemicalclusterofsingaporeresult',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='source_link',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='gmasscampaignresult',
            name='email_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='zerobounceresult',
            name='email_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
