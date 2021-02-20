# Generated by Django 3.1.2 on 2020-12-15 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_language'),
        ('relationships', '0029_auto_20201214_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='addresses', related_query_name='addresses', to='common.language'),
        ),
    ]
