# Generated by Django 3.0.2 on 2020-03-15 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterField(
            model_name='agent',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='wechat_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='wechat_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='whatsapp_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
