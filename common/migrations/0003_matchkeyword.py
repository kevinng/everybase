# Generated by Django 3.1.2 on 2021-05-27 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0064_auto_20210516_0155'),
        ('common', '0002_auto_20210516_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('keyword', models.CharField(db_index=True, max_length=200)),
                ('tolerance', models.IntegerField(db_index=True)),
                ('product_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='match_keywords', related_query_name='match_keywords', to='relationships.producttype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]