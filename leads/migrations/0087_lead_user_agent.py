# Generated by Django 3.1.2 on 2022-04-13 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0055_auto_20220411_1806'),
        ('leads', '0086_leadquerylog_user_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='user_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='leads', related_query_name='leads', to='relationships.useragent'),
        ),
    ]
