# Generated by Django 3.1.2 on 2021-04-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20210427_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='is_function',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
