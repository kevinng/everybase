# Generated by Django 3.1.2 on 2022-01-27 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0009_auto_20220127_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='goods_string',
            field=models.TextField(blank=True, null=True),
        ),
    ]
