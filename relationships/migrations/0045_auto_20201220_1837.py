# Generated by Django 3.1.2 on 2020-12-20 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0044_remove_link_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='link',
            field=models.URLField(db_index=True, unique=True),
        ),
    ]
