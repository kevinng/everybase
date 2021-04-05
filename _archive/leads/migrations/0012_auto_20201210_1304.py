# Generated by Django 3.1.2 on 2020-12-10 05:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_auto_20201210_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandcommission',
            name='received',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demandquote',
            name='received',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplycommission',
            name='received',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplyquote',
            name='received',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]