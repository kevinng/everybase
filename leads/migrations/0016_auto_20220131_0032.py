# Generated by Django 3.1.2 on 2022-01-30 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('leads', '0015_auto_20220130_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentquery',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='agent_queries', related_query_name='agent_queries', to='common.country'),
        ),
    ]
