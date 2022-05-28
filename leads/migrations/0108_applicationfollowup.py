# Generated by Django 3.1.2 on 2022-05-16 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0107_auto_20220516_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='follow_ups', related_query_name='follow_ups', to='leads.application')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]