# Generated by Django 3.1.2 on 2022-07-09 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0126_auto_20220703_2333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='is_line',
            new_name='via_line',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='line_id',
            new_name='via_line_id',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='is_telegram',
            new_name='via_telegram',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='telegram_username',
            new_name='via_telegram_username',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='is_viber',
            new_name='via_viber',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='is_other',
        ),
    ]
