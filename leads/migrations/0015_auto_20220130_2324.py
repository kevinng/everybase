# Generated by Django 3.1.2 on 2022-01-30 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0013_auto_20220130_2324'),
        ('leads', '0014_auto_20220129_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentquery',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='agent_query', related_query_name='agent_query', to='relationships.user'),
        ),
        migrations.AlterField(
            model_name='ineedagentquery',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='i_need_agent_query', related_query_name='i_need_agent_query', to='relationships.user'),
        ),
    ]