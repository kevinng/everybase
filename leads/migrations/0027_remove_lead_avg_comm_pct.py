# Generated by Django 3.1.2 on 2022-02-15 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0026_auto_20220212_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='avg_comm_pct',
        ),
    ]
