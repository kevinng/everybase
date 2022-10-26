# Generated by Django 3.1.2 on 2022-10-03 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_auto_20220301_2226'),
        ('relationships', '0088_user_business_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewCommentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='ReviewResponse',
            new_name='ReviewComment',
        ),
        migrations.DeleteModel(
            name='ReviewResponseImage',
        ),
        migrations.AddField(
            model_name='reviewcommentimage',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images_as_review_comment', related_query_name='images_as_review_comment', to='relationships.reviewcomment'),
        ),
        migrations.AddField(
            model_name='reviewcommentimage',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_response_images_as_file', related_query_name='review_response_images_as_file', to='files.file'),
        ),
    ]