# Generated by Django 3.1.2 on 2022-07-14 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0149_auto_20220715_0029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leadqueryaction',
            old_name='verified_user_country_only',
            new_name='verified_user_country',
        ),
    ]