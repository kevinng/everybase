# Generated by Django 3.1.2 on 2022-07-13 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0069_auto_20220707_1824'),
        ('leads', '0140_auto_20220713_1909'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='leadflag',
            unique_together={('lead', 'type', 'session_key', 'user')},
        ),
    ]
