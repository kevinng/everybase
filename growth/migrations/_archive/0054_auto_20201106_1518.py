# Generated by Django 3.1.2 on 2020-11-06 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0053_auto_20201106_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='category',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='description',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='email',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='email_domain',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='lead_type',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='source_link',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='sub_category',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]