# Generated by Django 3.1.2 on 2022-05-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0112_auto_20220524_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadquery',
            name='category',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
