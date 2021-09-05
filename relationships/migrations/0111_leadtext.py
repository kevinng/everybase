# Generated by Django 3.1.2 on 2021-09-05 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0110_user_current_lead'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('text', models.TextField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='texts', related_query_name='texts', to='relationships.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
