# Generated by Django 3.1.2 on 2020-11-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0011_auto_20201107_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
    ]