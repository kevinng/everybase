# Generated by Django 3.1.2 on 2022-02-24 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0055_search_to_user_ratio_20220224_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='search_appearance_count',
            field=models.IntegerField(db_index=True, default=1),
        ),
    ]
