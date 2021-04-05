# Generated by Django 3.1.2 on 2020-11-06 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0012_file_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedemandtype',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='filedemandtype',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fileissuetype',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fileissuetype',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='filepersontype',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='filepersontype',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='filesupplytype',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='filesupplytype',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='filetag',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='filetag',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]