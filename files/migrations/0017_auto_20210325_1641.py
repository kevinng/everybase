# Generated by Django 3.1.2 on 2021-03-25 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0016_auto_20201211_1354'),
        ('communications', '0014_auto_20210325_1841')
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileissue',
            name='file',
        ),
        migrations.RemoveField(
            model_name='fileissue',
            name='issue',
        ),
        migrations.RemoveField(
            model_name='fileissue',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='fileperson',
            name='file',
        ),
        migrations.RemoveField(
            model_name='fileperson',
            name='person',
        ),
        migrations.RemoveField(
            model_name='fileperson',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='filesupply',
            name='file',
        ),
        migrations.RemoveField(
            model_name='filesupply',
            name='rtype',
        ),
        migrations.RemoveField(
            model_name='filesupply',
            name='supply',
        ),
        migrations.RemoveField(
            model_name='filetag',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='file',
            name='demands',
        ),
        migrations.RemoveField(
            model_name='file',
            name='details_md',
        ),
        migrations.RemoveField(
            model_name='file',
            name='issues',
        ),
        migrations.RemoveField(
            model_name='file',
            name='persons',
        ),
        migrations.RemoveField(
            model_name='file',
            name='supplies',
        ),
        migrations.RemoveField(
            model_name='file',
            name='tags',
        ),
        migrations.DeleteModel(
            name='FileDemand',
        ),
        migrations.DeleteModel(
            name='FileDemandType',
        ),
        migrations.DeleteModel(
            name='FileIssue',
        ),
        migrations.DeleteModel(
            name='FileIssueType',
        ),
        migrations.DeleteModel(
            name='FilePerson',
        ),
        migrations.DeleteModel(
            name='FilePersonType',
        ),
        migrations.DeleteModel(
            name='FileSupply',
        ),
        migrations.DeleteModel(
            name='FileSupplyType',
        ),
        migrations.DeleteModel(
            name='FileTag',
        ),
    ]
