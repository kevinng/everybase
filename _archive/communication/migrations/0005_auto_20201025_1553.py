# Generated by Django 3.1.2 on 2020-10-25 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0004_issuestatus_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='issues', related_query_name='issues', to='communication.IssueTag'),
        ),
    ]