# Generated by Django 3.1.2 on 2022-04-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0057_manual_drop_company_name_vec_20220421_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
    ]