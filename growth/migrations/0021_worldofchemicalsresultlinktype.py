# Generated by Django 3.1.2 on 2020-10-23 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0020_worldofchemicalsresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorldOfChemicalsResultLinkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details_md', models.TextField(blank=True, null=True, verbose_name='Details in Markdown')),
                ('programmatic_key', models.CharField(blank=True, max_length=100, null=True)),
                ('programmatic_details_md', models.TextField(blank=True, null=True, verbose_name='Programmatic details in Markdown')),
            ],
            options={
                'verbose_name': 'WorldOfChemicalsResult-Link Type',
                'verbose_name_plural': 'WorldOfChemicalsResult-Link Types',
            },
        ),
    ]
