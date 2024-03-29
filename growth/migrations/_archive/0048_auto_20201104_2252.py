# Generated by Django 3.1.2 on 2020-11-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0047_auto_20201104_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookchemresult',
            name='harvested',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='business_type',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='city',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='contact_person',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='country_region',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='coy_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='email',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='mobile',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='province_state',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='qq',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='tel',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='website',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookchemresult',
            name='zip_code',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]
