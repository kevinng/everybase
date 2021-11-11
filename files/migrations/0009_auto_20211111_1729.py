# Generated by Django 3.1.2 on 2021-11-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0017_auto_20211111_1729'),
        ('relationships', '0160_auto_20211103_2126'),
        ('files', '0008_auto_20211110_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='files', related_query_name='files', to='leads.lead'),
        ),
        migrations.CreateModel(
            name='FileAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('access_count', models.IntegerField(db_index=True)),
                ('accessor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='file_accesses', related_query_name='file_accesses', to='relationships.user')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accesses', related_query_name='accesses', to='files.file')),
            ],
            options={
                'unique_together': {('file', 'accessor')},
            },
        ),
    ]
