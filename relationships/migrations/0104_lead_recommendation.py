# Generated by Django 3.1.2 on 2021-08-29 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_matchkeyword_country'),
        ('relationships', '0103_auto_20210822_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('display_text', models.TextField(blank=True, null=True)),
                ('capture_method_type', models.CharField(choices=[('manual', 'Manual'), ('menu_option', 'Menu Option')], db_index=True, max_length=50)),
                ('lead_type', models.CharField(choices=[('demand', 'Demand'), ('supply', 'Supply')], db_index=True, max_length=50)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='leads', related_query_name='leads', to='common.country')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='leads', related_query_name='leads', to='relationships.user')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='leads', related_query_name='leads', to='common.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('interested_product_type', models.BooleanField(blank=True, null=True)),
                ('responded_interested_product_type', models.DateTimeField(blank=True, null=True)),
                ('is_direct', models.BooleanField(blank=True, null=True)),
                ('responded_is_direct', models.DateTimeField(blank=True, null=True)),
                ('can_source', models.BooleanField(blank=True, null=True)),
                ('responded_can_source', models.DateTimeField(blank=True, null=True)),
                ('not_interested_details', models.BooleanField(blank=True, null=True)),
                ('responded_not_interested_details', models.DateTimeField(blank=True, null=True)),
                ('not_interested_details_reason', models.TextField(blank=True, null=True)),
                ('responded_not_interested_details_reason', models.DateTimeField(blank=True, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recommendations', related_query_name='recommendations', to='relationships.lead')),
                ('recommendee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recommendations', related_query_name='recommendations', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
