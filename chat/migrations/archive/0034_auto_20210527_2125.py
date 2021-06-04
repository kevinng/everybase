# Generated by Django 3.1.2 on 2021-05-27 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0033_auto_20210527_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageDataValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('value_string', models.CharField(db_index=True, max_length=200)),
                ('value_float', models.FloatField(db_index=True)),
                ('value_boolean', models.BooleanField(db_index=True)),
                ('is_valid', models.BooleanField(blank=True, db_index=True, null=True)),
                ('data_key', models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING', 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING'), ('NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING', 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING')], db_index=True, max_length=200)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='strings', related_query_name='strings', to='chat.messagedataset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='messagedatafloat',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='messagedatastring',
            name='dataset',
        ),
        migrations.DeleteModel(
            name='MessageDataBoolean',
        ),
        migrations.DeleteModel(
            name='MessageDataFloat',
        ),
        migrations.DeleteModel(
            name='MessageDataString',
        ),
    ]