# Generated by Django 3.1.2 on 2021-04-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0032_auto_20210427_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='notes',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='productspecificationtype',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
