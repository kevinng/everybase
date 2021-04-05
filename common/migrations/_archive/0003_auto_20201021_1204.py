# Generated by Django 3.0.5 on 2020-10-21 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_state_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='states', related_query_name='states', to='common.Country'),
        ),
    ]