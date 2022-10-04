# Generated by Django 3.1.2 on 2022-10-03 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('files', '0008_auto_20220301_2226'),
        ('relationships', '0086_auto_20220916_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactAction',
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
        migrations.CreateModel(
            name='DetailView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('count', models.IntegerField(db_index=True, default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('rating', models.CharField(choices=[('good', 'Good Review'), ('bad', 'Bad Review')], db_index=True, max_length=40)),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews_as_image', related_query_name='reviews_as_image', to='files.file')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', related_query_name='images', to='relationships.review')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewResponseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_response_images_as_file', related_query_name='review_response_images_as_file', to='files.file')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images_as_review_response', related_query_name='images_as_review_response', to='relationships.reviewresponse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='alertexcludecountry',
            name='alert',
        ),
        migrations.RemoveField(
            model_name='alertexcludecountry',
            name='country',
        ),
        migrations.RemoveField(
            model_name='alertkeyphrase',
            name='alert',
        ),
        migrations.RemoveField(
            model_name='alertkeyphrase',
            name='key_phrase',
        ),
        migrations.RemoveField(
            model_name='alertmatch',
            name='alert',
        ),
        migrations.RemoveField(
            model_name='alertmatch',
            name='requirement',
        ),
        migrations.RemoveField(
            model_name='requirement',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usercontactaction',
            name='contactee',
        ),
        migrations.RemoveField(
            model_name='usercontactaction',
            name='contactor',
        ),
        migrations.RemoveField(
            model_name='userdetailview',
            name='viewee',
        ),
        migrations.RemoveField(
            model_name='userdetailview',
            name='viewer',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='company_name',
            new_name='business_name',
        ),
        migrations.RemoveField(
            model_name='loginaction',
            name='type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='user',
            name='introduction',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slug_link',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slug_tokens',
        ),
        migrations.RemoveField(
            model_name='user',
            name='uuid',
        ),
        migrations.AddField(
            model_name='user',
            name='business_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users_as_country', related_query_name='users_as_country', to='common.country'),
        ),
        migrations.DeleteModel(
            name='Alert',
        ),
        migrations.DeleteModel(
            name='AlertExcludeCountry',
        ),
        migrations.DeleteModel(
            name='AlertKeyPhrase',
        ),
        migrations.DeleteModel(
            name='AlertMatch',
        ),
        migrations.DeleteModel(
            name='KeyPhrase',
        ),
        migrations.DeleteModel(
            name='Requirement',
        ),
        migrations.DeleteModel(
            name='UserContactAction',
        ),
        migrations.DeleteModel(
            name='UserDetailView',
        ),
        migrations.AddField(
            model_name='reviewresponse',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_responses_as_author', related_query_name='review_responses_as_author', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='reviewresponse',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='responses_as_review', related_query_name='responses_as_review', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews_as_reviewee', related_query_name='reviews_as_reviewee', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews_as_reviewer', related_query_name='reviews_as_reviewer', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='detailview',
            name='viewee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_detail_views', related_query_name='user_detail_views', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='detailview',
            name='viewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detail_views_as_viewer', related_query_name='detail_views_as_viewer', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='contactaction',
            name='contactee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contact_actions_as_contactees', related_query_name='contact_actions_as_contactees', to='relationships.user'),
        ),
        migrations.AddField(
            model_name='contactaction',
            name='contactor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contact_actions_as_contactor', related_query_name='contact_actions_as_contactor', to='relationships.user'),
        ),
    ]
