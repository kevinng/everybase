# Generated by Django 3.1.2 on 2022-03-15 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0073_remove_search_to_user_ratio_202203151438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='saved_count',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='search_to_user_details_count',
        ),
    ]
