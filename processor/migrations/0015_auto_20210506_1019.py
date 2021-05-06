# Generated by Django 3.1.2 on 2021-05-06 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0014_auto_20210505_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchingkeyword',
            name='case_sensitive',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='matchingkeyword',
            name='keyword',
            field=models.CharField(db_index=True, default='', max_length=200),
            preserve_default=False,
        ),
    ]
