# Generated by Django 3.1.2 on 2021-07-07 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_matchkeyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchkeyword',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='match_keywords', related_query_name='match_keywords', to='common.country'),
        ),
    ]
