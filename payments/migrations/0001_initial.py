# Generated by Django 3.1.2 on 2021-04-20 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
