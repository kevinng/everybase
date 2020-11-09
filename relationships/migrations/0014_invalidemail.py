# Generated by Django 3.1.2 on 2020-11-09 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_importjob_description'),
        ('relationships', '0013_email_import_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvalidEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('email', models.CharField(db_index=True, max_length=100, unique=True)),
                ('import_job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invalid_emails', related_query_name='invalid_emails', to='common.importjob')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
