# Generated by Django 3.0.5 on 2020-10-08 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0002_auto_20201008_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
