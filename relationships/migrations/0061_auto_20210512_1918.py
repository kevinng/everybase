# Generated by Django 3.1.2 on 2021-05-12 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # ('payments', '0008_auto_20210512_1203'),
        ('relationships', '0060_auto_20210512_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('product_type_captured', models.TextField(blank=True, null=True)),
                ('country_state_captured', models.TextField(blank=True, null=True)),
                ('packing_captured', models.TextField(blank=True, null=True)),
                ('quantity_captured', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(blank=True, db_index=True, null=True)),
                ('price_captured', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demands', related_query_name='demands', to='relationships.country')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demands', related_query_name='demands', to='payments.currency')),
                ('next_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_next_versions', related_query_name='demand_next_versions', to='relationships.demand')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
                ('demand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='matches', related_query_name='matches', to='relationships.demand')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='states', related_query_name='states', to='relationships.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('duration_uom', models.CharField(choices=[('d', 'Day'), ('w', 'Week'), ('m', 'Month')], db_index=True, max_length=2)),
                ('duration', models.FloatField(blank=True, db_index=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, db_index=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
                ('plural_name', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='unit_of_measures', related_query_name='unit_of_measures', to='relationships.producttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('product_type_captured', models.TextField(blank=True, null=True)),
                ('country_state_captured', models.TextField(blank=True, null=True)),
                ('availability_captured', models.TextField(blank=True, null=True)),
                ('packing_captured', models.TextField(blank=True, null=True)),
                ('quantity_captured', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(blank=True, db_index=True, null=True)),
                ('preorder_timeframe_captured', models.TextField(blank=True, null=True)),
                ('price_captured', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('deposit_percentage_captured', models.TextField(blank=True, null=True)),
                ('deposit_percentage', models.FloatField(blank=True, null=True)),
                ('accept_lc_captured', models.TextField(blank=True, null=True)),
                ('accept_lc', models.BooleanField(blank=True, null=True)),
                ('availability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.availability')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.country')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='payments.currency')),
                ('next_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_next_versions', related_query_name='supply_next_versions', to='relationships.supply')),
                ('packing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.unitofmeasure')),
                ('preorder_timeframe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.timeframe')),
                ('previous_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supply_previous_versions', related_query_name='supply_previous_versions', to='relationships.supply')),
                ('product_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.producttype')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.state')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supplies', related_query_name='supplies', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswerPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
                ('asked', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('sent_answerer', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('answered', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('question_captured', models.TextField()),
                ('question_rewrote', models.TextField(blank=True, null=True)),
                ('answer_captured', models.TextField(blank=True, db_index=True, null=True)),
                ('answer_rewrote', models.TextField(blank=True, null=True)),
                ('answerer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_answer_pair_answerers', related_query_name='question_answer_pair_answerers', to='relationships.user')),
                ('asker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_answer_pair_askers', related_query_name='question_answer_pair_askers', to='relationships.user')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_answer_pairs', related_query_name='question_answer_pairs', to='relationships.match')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='match',
            name='supply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='matches', related_query_name='matches', to='relationships.supply'),
        ),
        migrations.AddField(
            model_name='demand',
            name='packing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demands', related_query_name='demands', to='relationships.unitofmeasure'),
        ),
        migrations.AddField(
            model_name='demand',
            name='previous_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demand_previous_versions', related_query_name='demand_previous_versions', to='relationships.demand'),
        ),
        migrations.AddField(
            model_name='demand',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demands', related_query_name='demands', to='relationships.producttype'),
        ),
        migrations.AddField(
            model_name='demand',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demands', related_query_name='demands', to='relationships.state'),
        ),
        migrations.AddField(
            model_name='demand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demands', related_query_name='demands', to='relationships.user'),
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
                ('user_1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='connection_user_1s', related_query_name='connection_user_1s', to='relationships.user')),
                ('user_2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='connection_user_2s', related_query_name='connection_user_2s', to='relationships.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
