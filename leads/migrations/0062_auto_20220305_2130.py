# Generated by Django 3.1.2 on 2022-03-05 13:30

from django.db import migrations, models
import leads.models

def _uuid_str():
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0061_auto_20220305_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='slug_link',
            field=models.CharField(db_index=True, default=_uuid_str, max_length=64, null=True),
        ),
    ]
