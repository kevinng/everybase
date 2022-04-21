# Generated by Django 3.1.2 on 2022-02-27 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0040_auto_20220228_0018'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user DROP COLUMN company_name_vec CASCADE;
            '''
        ),
        migrations.AlterField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
    ]