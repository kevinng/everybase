# Generated by Django 3.1.2 on 2021-07-15 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0090_auto_20210714_1718'),
        ('payments', '0019_auto_20210619_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('programmatic_key', models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True)),
                ('programmatic_details', models.TextField(blank=True, null=True, verbose_name='Programmatic details')),
            ],
            options={
                'verbose_name': 'Price',
                'verbose_name_plural': 'Prices',
            },
        ),
        migrations.AlterModelOptions(
            name='paymenthash',
            options={'verbose_name': 'Payment hash', 'verbose_name_plural': 'Payment hashes'},
        ),
        migrations.AlterField(
            model_name='paymenthash',
            name='match',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='payment_links', related_query_name='payment_links', to='relationships.match'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='paymenthash',
            unique_together={('user', 'match')},
        ),
        migrations.RemoveField(
            model_name='paymenthash',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='paymenthash',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='paymenthash',
            name='unit_amount',
        ),
    ]