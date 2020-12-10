# Generated by Django 3.1.2 on 2020-12-10 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0014_auto_20201210_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplycommission',
            name='quotes',
        ),
        migrations.AddField(
            model_name='supplycommission',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='commissions', related_query_name='commissions', to='leads.supplyquote'),
        ),
    ]
