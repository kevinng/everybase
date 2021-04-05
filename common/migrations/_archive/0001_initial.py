# Generated by Django 3.0.5 on 2020-10-21 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details_md', models.TextField(blank=True, null=True, verbose_name='Details in Markdown')),
                ('programmatic_key', models.CharField(blank=True, max_length=100, null=True)),
                ('programmatic_details_md', models.TextField(blank=True, null=True, verbose_name='Programmatic details in Markdown')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details_md', models.TextField(blank=True, null=True, verbose_name='Details in Markdown')),
                ('programmatic_key', models.CharField(blank=True, max_length=100, null=True)),
                ('programmatic_details_md', models.TextField(blank=True, null=True, verbose_name='Programmatic details in Markdown')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]