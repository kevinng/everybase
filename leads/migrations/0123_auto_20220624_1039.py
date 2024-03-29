# Generated by Django 3.1.2 on 2022-06-24 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('leads', '0122_auto_20220622_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contacts', related_query_name='contacts', to='common.country'),
        ),
        migrations.AddField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
    ]
