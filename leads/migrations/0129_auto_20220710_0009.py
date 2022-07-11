# Generated by Django 3.1.2 on 2022-07-09 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0128_auto_20220709_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='is_wechat',
            new_name='via_wechat',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='wechat_id',
            new_name='via_wechat_id',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='is_whatsapp',
            new_name='via_whatsapp',
        ),
        migrations.AddField(
            model_name='contact',
            name='buying_help_find_buyers',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='buying_other',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='buying_promoting_goods',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='logistics_agent_need_logistics',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='logistics_agent_other',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sales_agent_cooperate_as_agent',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sales_agent_other',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sales_agent_recruiting_agents',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sales_agent_sourcing_goods',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='selling_help_find_sellers',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='selling_other',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='selling_sourcing_goods',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sourcing_agent_cooperate_as_agent',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sourcing_agent_other',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sourcing_agent_promoting_goods',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='sourcing_agent_recruiting_agents',
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
    ]
