# Generated by Django 3.1.2 on 2021-05-27 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0067_unitofmeasure_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmeasure',
            name='priority',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]