# Generated by Django 3.1.2 on 2021-05-05 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0037_location_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='company',
            name='notes',
        ),
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='programmatic_details',
            field=models.TextField(blank=True, null=True, verbose_name='Programmatic details'),
        ),
        migrations.AddField(
            model_name='company',
            name='programmatic_key',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]
