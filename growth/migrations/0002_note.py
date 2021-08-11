# Generated by Django 3.1.2 on 2021-08-10 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0093_auto_20210809_2210'),
        ('growth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('done', models.DateTimeField(blank=True, null=True)),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='growth_notes', related_query_name='growth_notes', to='relationships.email')),
                ('phone_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='growth_notes', related_query_name='growth_notes', to='relationships.phonenumber')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]