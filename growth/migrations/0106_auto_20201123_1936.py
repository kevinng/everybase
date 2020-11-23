# Generated by Django 3.1.2 on 2020-11-23 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0018_auto_20201120_1304'),
        ('growth', '0105_auto_20201123_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmassemailstatus',
            name='invalid_email',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gmass_email_status', related_query_name='gmass_email_status', to='relationships.invalidemail'),
        ),
    ]
