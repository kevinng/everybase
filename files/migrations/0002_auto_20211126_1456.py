# Generated by Django 3.1.2 on 2021-11-26 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relationships', '0001_initial'),
        ('leads', '0001_initial'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileaccess',
            name='accessor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='file_accesses', related_query_name='file_accesses', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='fileaccess',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accesses', related_query_name='accesses', to='files.file'),
        ),
        migrations.AddField(
            model_name='file',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='files', related_query_name='files', to='leads.lead'),
        ),
        migrations.AddField(
            model_name='file',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uploaded_files', related_query_name='uploaded_files', to='relationships.user'),
        ),
        migrations.AlterUniqueTogether(
            name='fileaccess',
            unique_together={('file', 'accessor')},
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together={('s3_bucket_name', 's3_object_key')},
        ),
    ]
