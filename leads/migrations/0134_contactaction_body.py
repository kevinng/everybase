# Generated by Django 3.1.2 on 2022-07-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0133_auto_20220710_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactaction',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
