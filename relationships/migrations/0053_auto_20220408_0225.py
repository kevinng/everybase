# Generated by Django 3.1.2 on 2022-04-07 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0052_remove_user_saved_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='search_to_user_count',
            new_name='clicks',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='search_appearance_count',
            new_name='impressions',
        ),
    ]
