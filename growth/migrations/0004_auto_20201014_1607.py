# Generated by Django 3.0.5 on 2020-10-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0020_auto_20201014_1454'),
        ('growth', '0003_auto_20201014_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='emails',
            field=models.ManyToManyField(blank=True, related_name='fibre2fashion_results', related_query_name='fibre2fashion_results', to='relationships.Email'),
        ),
        migrations.AlterField(
            model_name='fibre2fashionresult',
            name='links',
            field=models.ManyToManyField(blank=True, related_name='fibre2fashion_results', related_query_name='fibre2fashion_results', to='relationships.Link'),
        ),
    ]
