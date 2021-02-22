# Generated by Django 3.1.2 on 2021-01-06 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_auto_20201217_1310'),
        ('relationships', '0045_auto_20201220_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='links', related_query_name='links', to='common.language'),
        ),
    ]