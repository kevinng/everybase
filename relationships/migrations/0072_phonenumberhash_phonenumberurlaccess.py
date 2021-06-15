# Generated by Django 3.1.2 on 2021-06-15 07:36

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0071_auto_20210615_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumberHash',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phone_number_hashes', related_query_name='phone_number_hashes', to='relationships.phonenumber')),
                ('phone_number_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phone_number_hashes', related_query_name='phone_number_hashes', to='relationships.phonenumbertype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phone_number_hashes', related_query_name='phone_number_hashes', to='relationships.user')),
            ],
            options={
                'verbose_name': 'Phone Number Hash',
                'verbose_name_plural': 'Phone Number Hashes',
                'unique_together': {('user', 'phone_number_type', 'phone_number')},
                'index_together': {('user', 'phone_number_type', 'phone_number')},
            },
        ),
        migrations.CreateModel(
            name='PhoneNumberURLAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('accessed', models.DateTimeField(db_index=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
                ('is_mobile', models.BooleanField(blank=True, db_index=True, null=True)),
                ('is_tablet', models.BooleanField(blank=True, db_index=True, null=True)),
                ('is_touch_capable', models.BooleanField(blank=True, db_index=True, null=True)),
                ('is_pc', models.BooleanField(blank=True, db_index=True, null=True)),
                ('is_bot', models.BooleanField(blank=True, db_index=True, null=True)),
                ('browser', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('browser_family', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('browser_version', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('browser_version_string', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('os', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('os_version', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('os_version_string', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('device', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('device_family', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('hash', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accesses', related_query_name='accesses', to='relationships.phonenumberhash')),
            ],
            options={
                'verbose_name': 'Phone Number URL Access',
                'verbose_name_plural': 'Phone Number URL Accesses',
            },
        ),
    ]
