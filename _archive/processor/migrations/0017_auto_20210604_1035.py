# Generated by Django 3.1.2 on 2021-06-04 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0016_auto_20210506_1538'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MatchingKeyword',
        ),
        migrations.RemoveField(
            model_name='messagebodymetadataentity',
            name='meta_data',
        ),
        migrations.DeleteModel(
            name='MessageBodyMetaData',
        ),
        migrations.DeleteModel(
            name='MessageBodyMetaDataEntity',
        ),
        migrations.DeleteModel(
            name='TestMessage',
        ),
    ]