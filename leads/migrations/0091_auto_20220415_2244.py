# Generated by Django 3.1.2 on 2022-04-15 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0090_auto_20220414_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaddetailview',
            name='count',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
