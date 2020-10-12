# Generated by Django 3.0.5 on 2020-10-12 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0021_auto_20201010_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='invalidated_reason_md',
            field=models.TextField(blank=True, null=True, verbose_name='Invalidated reason in Markdown'),
        ),
        migrations.AlterField(
            model_name='demandcommission',
            name='invalidated_reason_md',
            field=models.TextField(blank=True, null=True, verbose_name='Invalidated reason in Markdown'),
        ),
        migrations.AlterField(
            model_name='demandquote',
            name='invalidated_reason_md',
            field=models.TextField(blank=True, null=True, verbose_name='Invalidated reason in Markdown'),
        ),
        migrations.AlterField(
            model_name='supply',
            name='invalidated_reason_md',
            field=models.TextField(blank=True, null=True, verbose_name='Invalidated reason in Markdown'),
        ),
        migrations.AlterField(
            model_name='supplycommission',
            name='invalidated_reason_md',
            field=models.TextField(blank=True, null=True, verbose_name='Invalidated reason in Markdown'),
        ),
        migrations.AlterField(
            model_name='supplyquote',
            name='invalidated_reason_md',
            field=models.TextField(blank=True, null=True, verbose_name='Invalidated reason in Markdown'),
        ),
    ]
