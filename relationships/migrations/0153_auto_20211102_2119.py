# Generated by Django 3.1.2 on 2021-11-02 13:19

from django.db import migrations, models
import django.db.models.deletion
import relationships.models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0152_remove_phonenumber_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('accessed', models.DateTimeField(auto_now=True, db_index=True)),
                ('token', models.CharField(db_index=True, default=relationships.models.get_token, max_length=200)),
                ('expiry_secs', models.IntegerField(db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='login_tokens', related_query_name='login_tokens', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('accessed', models.DateTimeField(auto_now=True, db_index=True)),
                ('token', models.CharField(db_index=True, default=relationships.models.get_token, max_length=200)),
                ('expiry_secs', models.IntegerField(db_index=True)),
                ('whatsapp_phone_number', models.CharField(db_index=True, max_length=50)),
                ('first_name', models.CharField(db_index=True, max_length=50)),
                ('last_name', models.CharField(db_index=True, max_length=50)),
                ('email', models.CharField(db_index=True, max_length=50)),
                ('languages_string', models.CharField(db_index=True, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='register_tokens', related_query_name='register_tokens', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='LoginRegisterToken',
        ),
    ]
